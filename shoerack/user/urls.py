from django.urls import path
from . import views

urlpatterns = [
   
    path('',views.index,name='index'),
    path('loginn',views.loginn,name = 'loginn'),
    path('register',views.register,name = 'register'),
    path('signoutt/',views.signoutt,name = 'signoutt'),
    path('otp',views.otpp,name ='otp'),
    path('productsample/',views.productsample,name='productsample'),
    path('singleproduct/<int:id>',views.singleproduct,name= 'singleproduct'),
    
]
