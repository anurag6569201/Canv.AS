from django.urls import path
from core import views

app_name="core"

urlpatterns=[
    # homepage
    path('',views.index,name='index'),
    path('products',views.product_list,name='product_list'),
    path('product/<pid>',views.product_detail,name='product_detail'),

    # category
    path('category',views.category_list,name='category_list'),
    path('category/<cid>',views.product_list_category,name='product_list_category'),

    path('vendor',views.vendor_list,name='vendor_list'),
    path('vendor/<vid>',views.vendor_detail,name='vendor_detail'),

    # tags
    path('product/tag/<slug:tag_slug>',views.tag_list,name='tags'),
] 