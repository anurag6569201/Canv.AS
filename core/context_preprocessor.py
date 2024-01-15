from core.models import Category, Vendor, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address

def default(request):
    categories=Category.objects.all()
    return {
        'category':categories,
    }