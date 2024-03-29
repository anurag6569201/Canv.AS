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

    # add review
    path('ajax-add-review/<pid>/',views.ajax_add_review,name="ajax-add-review"),

    # search
    path("search/",views.search_view,name="search"),

    #add to cart
    path("add-to-cart/",views.add_to_cart,name="add-to-cart"),
    path("cart/",views.cart_view,name="cart"),
    path("update-cart/",views.update_from_cart,name="update-cart"),

    path("checkout/success/",views.success,name="success"),


    path("dashboard/",views.customer_dashboard,name="customer_dashboard"),
    path("dashboard-edit/",views.dash,name="dash"),
    path("dashboard/order/<int:id>",views.order_detail_view,name="order-detail"),

    # address default
    path("make-default-address",views.make_address_default,name="make-default-address"),

    # contact
    path("contact/", views.contact, name="contactUs"),
] 