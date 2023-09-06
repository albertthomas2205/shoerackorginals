from django.urls import path
from . import views

urlpatterns = [
   
    path('',views.index,name='index'),
    path('loginn/',views.loginn,name = 'loginn'),
    path('register/',views.register,name = 'register'),
    path('signoutt/',views.signoutt,name = 'signoutt'),
    path('otp/',views.otpp,name ='otp'),
    path('productsample/',views.productsample,name='productsample'),
    path('base/',views.base,name ='base'),
    path('category/<int:id>',views.category,name= 'category'),
    path('details/', views.user_details, name='user_addresses'),
    path('shop',views.shop,name='shop'),
    path('edit_address/<int:userdetails_id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:userdetails_id>/', views.delete_address, name='delete_address'),
    path('productt/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('update_price/', views.update_price, name='update_price'),
    path('search',views.search, name = 'search'),
    path('category/search',views.search,name='categorysearch'),
    path('send_otp/',views.send_otp,name = 'send_otp'),
    path('verify_otp/',views.verify_otp, name = 'verify_otp'),
    path('singproduct/<int:id>',views.singproduct,name='singproduct'),
    path('productsize/<int:id>',views.productsize,name='productsize'),
    path('singproduct/cartaddjs/<int:id>/', views.cartaddjs, name='cartaddjs'),
    
    
]
