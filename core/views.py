from django.shortcuts import render,HttpResponse
from core.models import Category, Vendor, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address,RATING,profile
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from core.models import FAQS
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from django.db.models import Avg,Count
from core.forms import ProductReviewForm
from core.forms import addressForm
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
import razorpay
from django.conf import settings
from django.contrib import messages

import calendar
from django.db.models.functions import ExtractMonth

from userauths.models import User
from django.db.models.signals import post_save
from django.db.models.signals import post_save

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

@login_required
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

@login_required
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

@login_required
def search_view(request):
    query=request.GET.get("q")
    products=Product.objects.filter(tagsss__name__icontains=query).order_by("-date").distinct()
    
    context={
        'products':products,
        'query':query,
    }
    return render(request,"core/search.html",context)

@login_required
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

@login_required
def cart_view(request):
    cart_total_amount=0
    if 'cart_data_obj' in request.session:
        for product_id,item in request.session['cart_data_obj'].items():
            cart_total_amount+=int(item['qty'])*float(item['price'])
        
        client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
        payment=client.order.create({'amount':cart_total_amount*100,'currency':'INR','payment_capture':1})
       
        return render(request,"core/cart.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount,'payment':payment})
    else:
        return render(request,"core/cart.html",{"cart_data":'','totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})

@login_required
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
       
        
        context=render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount,'payment':payment})

        return JsonResponse({"data":context,'totalcartitems':len(request.session['cart_data_obj'])})
    
@login_required
def success(request):
    cart_total_amount=0
    if 'cart_data_obj' in request.session:
        for product_id,item in request.session['cart_data_obj'].items():
            cart_total_amount+=int(item['qty'])*float(item['price'])

        order = CartOrder.objects.create(
            user=request.user,  # Assign the user to the order
            price=cart_total_amount,
        )
        cart_total_amount=0
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_item = CartOrderItems.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price']),
                user=request.user,  # Assign the user to the CartOrderItem
            )
    return render(request,"core/success.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})

@login_required
def customer_dashboard(request):
    orders_list=CartOrder.objects.filter(user=request.user).order_by('-id')
    address=Address.objects.filter(user=request.user)
    address_form=addressForm()

    orders=CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month","count")
    month=[]
    total_order=[]

    for o in orders:
        month.append(calendar.month_name[o["month"]])
        total_order.append(o["count"])

    prof=profile.objects.get(user=request.user)
    if request.method=="POST":
        addr=request.POST.get("address")
        mobile=request.POST.get("mobile")
        new_address=Address.objects.create(
            user=request.user,
            address=addr,
            mobile=mobile,
        )
        messages.success(request,"address added successfully")
        return redirect("core:customer_dashboard")
    
    context={
        'profile':prof,
        'orders':orders_list,
        'address':address,
        'address_form':address_form,
        'ord':orders,
        'month':month,
        'total_order':total_order,
    }
    return render(request,'core/dashboard.html',context)

@login_required
def order_detail_view(request, id):
    try:
        order = CartOrder.objects.get(id=id, user=request.user)
        products = CartOrderItems.objects.filter(order=order)
        context = {
            "order": order,
            "products": products,
        }
        return render(request, 'core/order-detail.html', context)
    except CartOrder.DoesNotExist:
        return HttpResponse("Not found any order")

@login_required   
def make_address_default(request):
    id=request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean":True})

from .forms import profileForm

@login_required
def dash(request):
    proff = profile.objects.get(user=request.user)
    prof=profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = profileForm(request.POST, request.FILES, instance=proff)
        if form.is_valid():
            form.save()
            return redirect("core:customer_dashboard")
    else:
        form = profileForm(instance=proff)
    context = {
        'profile':prof,
        'dash_form': form,
    }
    return render(request, 'core/dashboardedit.html', context)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile,sender=User)