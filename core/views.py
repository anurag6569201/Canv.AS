from django.shortcuts import render,HttpResponse

from core.models import Category, Vendor, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address
# Create your views here.

def index(request):
    products=Product.objects.filter(product_status="publish",featured=True).order_by('-id')

    context={
        "products":products
    }

    return render(request,'core/index.html',context)

def product_list(request):
    products=Product.objects.filter(product_status="publish").order_by('-id')

    context={
        "products":products
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