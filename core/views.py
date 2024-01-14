from django.shortcuts import render,HttpResponse

from core.models import Category, Vendor, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address
# Create your views here.

def index(request):
    products=Product.objects.filter(product_status="publish",featured=True).order_by('-id')

    context={
        "products":products
    }

    return render(request,'core/index.html',context)