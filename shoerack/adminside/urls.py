from django.urls import path
from adminside import views


urlpatterns = [
   
    # path('account',views.adminsignup,name='account'),
    path('signin/',views.signin,name = 'signin'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('user/',views.user,name = 'user'),
    path('block/<int:id>',views.block_user_view,name= 'block'),
    path('base/',views.base,name='base'),
    path('product/',views.product,name='product'),
    path('signout/',views.signout,name = 'signout'),
    path('category/',views.category,name= 'category'),
    path('add_category/',views.add_category,name='add_category'),
    path('edit_category/<int:id>',views.edit_category,name='edit'),
    path('delete_category/<str:name>/',views.delete_category, name='delete_category'),
    path('add_sub/',views.add_sub,name='add_sub'),
    path('edit_sub/<int:id>',views.edit_category,name='edit'),
    path('delete_sub/<str:name>/', views.delete_sub, name='delete_category'),
    path('sub/',views.sub,name='sub'),
    path('add_product/',views.add_product,name= 'add_product'),
]
