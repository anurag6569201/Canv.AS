from django.urls import path
from core import views

app_name="core"

urlpatterns=[
    path('',views.index,name='index'),
    path('products',views.product_list,name='product_list'),
    path('category',views.category_list,name='category_list'),
    path('category/<cid>',views.product_list_category,name='product_list_category'),
] 