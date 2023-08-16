from django.urls import path
from . import views
urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='cart'),
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('car/',views.car,name='car'),
    path('order/',views.order,name='order'),
    path('cart/update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/createorder', views.create_order, name='createorder'),
    path('userorders',views.userorders,name='userorders'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('addwishlist/<int:id>/',views.Addwishlist,name='addwishlist'),
   
]
