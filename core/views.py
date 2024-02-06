from django.shortcuts import render,HttpResponse
from core.models import Category, Vendor, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address,RATING
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from core.models import FAQS
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from django.db.models import Avg
from core.forms import ProductReviewForm
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
import razorpay
from django.conf import settings

@login_required(login_url='/user/sign-in')
def index(request):
    products=Product.objects.filter(product_status="publish",featured=True).order_by('-id')
    faqs=FAQS.objects.all()
    context={
        "faqs":faqs,
        "products":products
    }
    return render(request,'core/index.html',context)

@login_required
def product_list(request):
    products=Product.objects.filter(product_status="publish").order_by('-id')
    product_count=Product.objects.filter(product_status="publish").order_by('-id')
    page=request.GET.get('page')
    num_of_items=8
    paginator=Paginator(products,num_of_items)

    try:
        products=paginator.page(page)
    except PageNotAnInteger:
        page=1
        products=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages
        products=paginator.page(page)

    context={
        "products":products,
        "paginator":paginator,
        "product_count":product_count,
    }

    return render(request,'core/product-list.html',context)

@login_required
def category_list(request):
    categories=Category.objects.all()

    context={
        "category":categories
    }

    return render(request,'core/category-list.html',context)

@login_required
def product_list_category(request,cid):
    category=Category.objects.get(cid=cid)
    products=Product.objects.filter(product_status="publish",category=category)

    context={
        "category":category,
        "products":products,
    }

    return render(request,"core/category-product-list.html",context)

@login_required
def vendor_list(request):
    vendors=Vendor.objects.all()
    context={
        "vendors":vendors,
    }
    return render(request,"core/vendor-list.html",context)

@login_required
def vendor_detail(request,vid):
    vendor=Vendor.objects.get(vid=vid)
    products=Product.objects.filter(product_status="publish",vendor=vendor)
    context={
        "vendor":vendor,
        "products":products,
    }
    return render(request,"core/vendor-detail.html",context)

@login_required
def product_detail(request,pid):
    product=Product.objects.get(pid=pid)
    related_product=Product.objects.filter(category=product.category).exclude(pid=pid)[:4]
    Addres=Address.objects.get(user=request.user)
    product_images = ProductImages.objects.filter(product=product)
    vendor = product.vendor

    # all review
    review=ProductReview.objects.filter(product=product).order_by("-date")

    # avg review
    avg_review=ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    total_reviews_count = review.count()

    # review form
    reivew_form=ProductReviewForm()

    star_rating_percentages = {}
    for rating, _ in RATING:
        rating_count = review.filter(rating=rating).count()
        percentage = (rating_count / total_reviews_count) * 100 if total_reviews_count != 0 else 0
        star_rating_percentages[rating] = percentage

    context={
        "vendor":vendor,
        "product":product,
        "product_images":product_images,
        "Addres":Addres,
        "review":review,
        "avg_review":avg_review,
        'star_rating_percentages': star_rating_percentages,
        "related_product":related_product,
        'reivew_form':reivew_form,
    }
    return render(request,"core/product-detail.html",context)

def tag_list(request, tag_slug=None):
    tag = None
    products=Product.objects.filter(product_status="publish").order_by('-id')
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tagsss=tag)

    context = {
        "prod": products,
        "tag": tag,
    }
    return render(request, "core/tag.html", context)

def ajax_add_review(request,pid):
    product=Product.objects.get(pid=pid)
    user=request.user

    review=ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
    )

    context={
        'user':user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],
    }

    avg_review=ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    return redirect("core:product_detail", pid=product.pid)

def search_view(request):
    query=request.GET.get("q")
    products=Product.objects.filter(tagsss__name__icontains=query).order_by("-date").distinct()
    
    context={
        'products':products,
        'query':query,
    }
    return render(request,"core/search.html",context)

def add_to_cart(request):
    cart_product={}
    cart_product[str(request.GET['id'])]={
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
        'pid':request.GET['product_pid'],
        'image':request.GET['product_image'],
    }
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data=request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty']=int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj']=cart_data
        else:
            cart_data=request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj']=cart_data
    else:
        request.session['cart_data_obj']=cart_product
    
    return JsonResponse({"data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amount=0
    if 'cart_data_obj' in request.session:
        for product_id,item in request.session['cart_data_obj'].items():
            cart_total_amount+=int(item['qty'])*float(item['price'])
        
        client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
        payment=client.order.create({'amount':cart_total_amount*100,'currency':'INR','payment_capture':1})
        cart_order, created = CartOrder.objects.get_or_create(user=request.user)
        cart_order.price = cart_total_amount  # Update the total price if necessary
        cart_order.save()
       
        return render(request,"core/cart.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount,'payment':payment})
    else:
        return render(request,"core/cart.html",{"cart_data":'','totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})


def update_from_cart(request):
    product_id=str(request.GET['id'])
    product_qty=str(request.GET['qty'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data=request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty']=product_qty
            request.session['cart_data_obj']=cart_data

    cart_total_amount=0
    if 'cart_data_obj' in request.session:
        for product_id,item in request.session['cart_data_obj'].items():
            cart_total_amount+=int(item['qty'])*float(item['price'])
        
        client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
        payment=client.order.create({'amount':cart_total_amount*100,'currency':'INR','payment_capture':1})
        cart_order, created = CartOrder.objects.get_or_create(user=request.user)
        cart_order.price = cart_total_amount  # Update the total price if necessary
        cart_order.save()
       
        
        context=render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount,'payment':payment})

        return JsonResponse({"data":context,'totalcartitems':len(request.session['cart_data_obj'])})
    

def success(request):
    order_id=request.GET.get('order_id')
    cart=CartOrder.objects.get(razor_pay_order_id=order_id)
    cart.paid_track=True
    cart.save()
    return HttpResponse("Payment success")