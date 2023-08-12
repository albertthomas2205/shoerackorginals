from django.urls import path
from . import views

urlpatterns = [
   
    path('',views.index,name='index'),
    path('loginn/',views.loginn,name = 'loginn'),
    path('register/',views.register,name = 'register'),
    path('signoutt/',views.signoutt,name = 'signoutt'),
    path('otp/',views.otpp,name ='otp'),
    path('productsample/',views.productsample,name='productsample'),
    # path('singleproduct/<int:id>',views.singleproduct,name= 'singleproduct'),
    path('base/',views.base,name ='base'),
    # path('address/',views.profile, name= 'address'),
    path('category/<int:id>',views.category,name= 'category'),
    # path('add_address/', views.add_address, name='add_address'),
    # path('profile/',views.profile,name='profile'),
    path('details/', views.user_details, name='user_addresses'),
    path('shop',views.shop,name='shop'),
    # path('add_address/', views.add_address, name='add_address'),
    path('edit_address/<int:userdetails_id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:userdetails_id>/', views.delete_address, name='delete_address'),
    path('productt/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('update_price/', views.update_price, name='update_price'),
    
]
