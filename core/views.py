from django.shortcuts import render,HttpResponse

from core.models import Category, Vendor, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address
# Create your views here.

def index(request):
    products=Product.object.all()

    context={
        "products":products
    }

    return render(request,'core/index.html',context)