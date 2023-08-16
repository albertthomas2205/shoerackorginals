from django.urls import path
from adminside import views


urlpatterns = [
  
    path('signin/',views.signin,name = 'signin'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('user/',views.user,name = 'user'),
    path('block/<int:id>',views.block_user_view,name= 'block'),
    path('base/',views.base,name='base'),
    path('product/',views.product,name='product'),
    path('signout/',views.signout,name = 'signout'),
    path('category/',views.category,name= 'category'),
    # path('add_category/',views.add_category,name='add_category'),
    # path('delete_category/<str:name>/',views.delete_category, name='delete_category'),
    # path('delete_brand/<int:brand_id>/', views.delete_brand, name='delete_brand'),
    # path('sub/',views.sub,name='sub'),
    path('add_product/',views.add_product,name= 'add_product'),
    path('edit_productsize/<int:id>/size/<int:size_id>/', views.productsize, name='edit_productsize'),
    # path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    # path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'), 
    path('product_list/', views.product_list, name='product_list'),
    path('category/addbrand',views.addbrand,name='addbrand'),
    path('product/addproduct',views.addproduct,name = 'addproduct'),
    path('product/productsize/<int:id>',views.productsize,name = 'productsize'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('deletecategory/<int:category_id>/', views.delete_category, name='delete_category'),
    path('ordermanagement/',views.Orders,name='ordermanagement'),
    path('update_order_status/<int:id>/',views.update_order_status,name='update_order_status'),
    path('delete_product_size/<int:id>/', views.delete_product_size, name='delete_product_size'),
    path('editvarient/<int:id>/',views.editproductsize,name='editvarient')


]
