from django.urls import path
from . import views

urlpatterns = [

    
    path('profilehome/', views.profilehome, name='profilehome'),
    path('viewadd/',views.viewaddress,name= 'viewaddress'),
    path('addaddress/',views.addaddress,name='addaddress'),
    path('delete_address/', views.delete_address, name='delete_address'),
    path('editaddress/<int:userdetails_id>',views.editaddress,name='editaddress'),
    path('userorders/',views.userorders,name='userorders'),
    path('usercancel/<int:id>/',views.Usercancel,name='usercancel'),
    path('forgot/',views.forgot,name='forgot'),
    path('forgototp/',views.forgototp,name='forgototp'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('resendotp/',views.Resendotp,name='resendotp'),
    path('resetpassword/',views.resetpassword,name='resetpassword')
]
