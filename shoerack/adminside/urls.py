from django.urls import path
from adminside import views


urlpatterns = [
  
    path('signin/',views.signin,name = 'signin'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('user/',views.user,name = 'user'),
    path('block/<int:id>',views.block_user_view,name= 'block'),
    path('product/',views.product,name='product'),
    path('signout/',views.signout,name = 'signout'),
    path('category/',views.category,name= 'category'),
    path('product_list/', views.product_list, name='product_list'),
    path('category/addbrand',views.addbrand,name='addbrand'),
    path('product/addproduct',views.addproduct,name = 'addproduct'),
    path('product/productsize/<int:id>',views.productsizee,name = 'productsizee'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('deletecategory/<int:category_id>/', views.delete_category, name='delete_category'),
    path('update_order_status/<int:id>/',views.update_order_status,name='update_order_status'),
    path('delete_product_size/<int:id>/', views.delete_product_size, name='delete_product_size'),
    path('deactivatecoupon/<int:id>/', views.deactivatecoupon, name='deactivatecoupon'),
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
    

    path('monthly/',views.sales_monthly,name='monthly'),
    path('yearly/',views.sales_yearly,name='yearly'),
    path('daily/',views.sales_daily,name='daily'),
    path('daily_sales/',views.daily_sales,name='dailysales'),
    path('sales_report/',views.sales_report,name='sales_report'),
    
    
    
    path('orderchartsdaily/', views.sales_chart_daily, name='orderchartsdaily'),
    path('orderchartsweekly/', views.sales_chart_weekly, name='orderchartsweekly'),
    path('orderchartsmonthly/', views.sales_chart_monthly, name='orderchartsmonthly'),
    
    
]
