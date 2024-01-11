from django.contrib import admin
from core.models import Category,Tags,Vendor,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,Wishlist,Address


# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model=ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImagesAdmin]
    list_display=['user','title','product_image','price','featured','product_status']

class CategoryAdmin(admin.ModelAdmin):
    list_display=['user','category_image']


class VendorAdmin(admin.ModelAdmin):
    list_display=['title','vendor_image']

class CartOrderAdmin(admin.ModelAdmin):
    list_display=['user','price','paid_status','order_date','product_status']


class CartOrderItemAdmin(admin.ModelAdmin):
    list_display=['user','invoice_no','item','image','qty','price','total']
    
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display=['user','product','review','rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display=['user','product','date']


class AddressAdmin(admin.ModelAdmin):
    list_display=['user','address','status']