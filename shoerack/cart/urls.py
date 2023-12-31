from django.urls import path
from . import views
urlpatterns = [
  
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.CartDetail, name='cart'),
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('cart/update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('createorder', views.create_order, name='createorder'),
    path('createorders', views.create_orders, name='createorders'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('removecoupon/', views.Removecoupon, name='removecoupon'),
    path('selectaddress', views.selectaddress, name='selectaddress'),
    path('thankyou',views.thanku,name='thankyou'),
    path('checkout/coin_add', views.coin_add, name='coin_add'),
    path('editaddress/<int:userdetails_id>',views.editaddr,name='editadd'),
   
   
   
    
]
