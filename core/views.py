from django.shortcuts import render,HttpResponse
from core.models import Category, Vendor, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from core.models import FAQS
def index(request):
    products=Product.objects.filter(product_status="publish",featured=True).order_by('-id')
    faqs=FAQS.objects.all()
    context={
        "faqs":faqs,
        "products":products
    }

    return render(request,'core/index.html',context)

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


def category_list(request):
    categories=Category.objects.all()

    context={
        "category":categories
    }

    return render(request,'core/category-list.html',context)

def product_list_category(request,cid):
    category=Category.objects.get(cid=cid)
    products=Product.objects.filter(product_status="publish",category=category)

    context={
        "category":category,
        "products":products,
    }

    return render(request,"core/category-product-list.html",context)

def vendor_list(request):
    vendors=Vendor.objects.all()
    context={
        "vendors":vendors,
    }
    return render(request,"core/vendor-list.html",context)


def vendor_detail(request,vid):
    vendor=Vendor.objects.get(vid=vid)
    products=Product.objects.filter(product_status="publish",vendor=vendor)
    context={
        "vendor":vendor,
        "products":products,
    }
    return render(request,"core/vendor-detail.html",context)


def product_detail(request,pid):
    product=Product.objects.get(pid=pid)
    product_images = ProductImages.objects.filter(product=product)
    vendor = product.vendor
    context={
        "vendor":vendor,
        "product":product,
        "product_images":product_images,
    }
    return render(request,"core/product-detail.html",context)