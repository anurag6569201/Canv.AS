from django.urls import path
from userauths import views

app_name='user_auths'

urlpatterns=[
    path('sign-up/',views.register_view,name='sign-up')
]