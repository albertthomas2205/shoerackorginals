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
    # path('add_product/',views.add_product,name= 'add_product'),
    path('product_list/', views.product_list, name='product_list'),
    path('category/addbrand',views.addbrand,name='addbrand'),
    path('product/addproduct',views.addproduct,name = 'addproduct'),
    path('product/productsize/<int:id>',views.productsize,name = 'productsize'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('deletecategory/<int:category_id>/', views.delete_category, name='delete_category'),
    path('update_order_status/<int:id>/',views.update_order_status,name='update_order_status'),
    path('delete_product_size/<int:id>/', views.delete_product_size, name='delete_product_size'),
    path('editvarient/<int:id>/',views.editproductsize,name='editvarient'),
    path('deleteproduct/<int:id>/',views.delete_product,name='deleteproduct'),
    path('admincoupon/', views.Admincoupon, name='admincoupon'),
    path('ordermanagement',views.Orders,name='ordermanagement'),
    path('order_cancel/<int:id>/', views.order_cancel, name='order_cancel'),
    path('adminorder_deatails/<int:id>/', views.adminorder_deatails, name='adminorder_deatails'),
    path('returns', views.Returns, name='returns'),
    path('returndetails/<int:id>/', views.returndetails, name='returndetails'),
    path('update_return_status/<int:id>/', views.update_return_status, name='update_return_status'),
    path('admindashboard',views.AdminDashboard,name='admindashboard'),
    
    path('chart/',views.chart,name='chart'),
    path('monthly/',views.sales_monthly,name='monthly'),
    path('yearly',views.yearly,name='yearly'),
    path('daily/',views.sales_daily,name='daily'),
    path('sales_report/',views.sales_report,name='sales_report'),
    
    
]
