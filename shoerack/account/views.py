from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from adminside.forms import UserdetailsForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from user.models import CustomUser,CustomUserManager
from account.models import Userdetails
from account.models import Order
from django.contrib.auth import authenticate
    



# Create your views here.
def profilehome(request):
    addresses = request.user
    
    return render(request,'profile/profilehome.html',{'addresses':addresses})


def viewaddress(request):
    # Retrieve the logged-in user's details
    addresses = Userdetails.objects.filter(userr=request.user)
    # Pass the user_details object to the HTML template
    return render(request, 'profile/viewadddress.html', {'addresses': addresses})

def addaddress(request):
    if request.method == 'POST':
        form = UserdetailsForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.userr = request.user  # Assuming you have a CustomUser model and using request.user for the logged-in user
            address.save()
            return redirect('viewaddress')  # Replace 'address_list' with the URL name of the page displaying the list of addresses
    else:
        form = UserdetailsForm()
    
    return render(request, 'profile/addaddress.html', {'form': form})

from django.http import JsonResponse

def delete_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        try:
            address = Userdetails.objects.get(pk=address_id)
            address.delete()
            return JsonResponse({'success': True})
        except Userdetails.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Address not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def editaddress(request, userdetails_id):
    userdetails = get_object_or_404(Userdetails, id=userdetails_id)

    if request.method == 'POST':
        form = UserdetailsForm(request.POST, instance=userdetails)
        if form.is_valid():
            form.save()
            return redirect('viewaddress')  # Replace with the URL name for success
    else:
        form = UserdetailsForm(instance=userdetails)

    context = {'form': form}
    return render(request, 'profile/editaddress.html', context)

# def userorders(request):
#     cust = get_object_or_404(CustomUser, id=request.user.id)
#     orders=Order.objects.filter(user=cust)
    
#     context={'orders':orders,'cust':cust}
#     return render(request,'profile/orders.html',context)

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

# def userorders(request):
#     cust = get_object_or_404(CustomUser, id=request.user.id)
#     orders = Order.objects.filter(user=cust)

#     # Number of items to show per page
#     items_per_page = 2  # You can adjust this number as per your preference

#     paginator = Paginator(orders, items_per_page)
    
#     page_number = request.GET.get('page')
#     page_orders = paginator.get_page(page_number)
    
#     context = {'page_orders': page_orders, 'cust': cust}
#     return render(request, 'profile/orders.html', context)


def userorders(request):
    cust = get_object_or_404(CustomUser, id=request.user.id)
    orders = Order.objects.filter(user=cust).order_by('-created_at')

    # Number of items to show per page
    items_per_page = 2  # You can adjust this number as per your preference

    paginator = Paginator(orders, items_per_page)
    
    page_number = request.GET.get('page')
    page_orders = paginator.get_page(page_number)
    
    context = {'page_orders': page_orders, 'cust': cust}
    return render(request, 'profile/orders.html', context)



def Usercancel(request,id):
    edit=get_object_or_404(Order,id=id)
    edit.status='C'
    edit.save()
    return redirect('userorders')
    
def forgototp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        if user_otp == stored_otp:
            return redirect('forgotpassword')
        else:
            key='2'
            messages.error(request, f'invalid otp. ({key})')
            return redirect('forgototp')
    email = request.session.get('gmail')
    context={'email':email}
    return render(request,'userside/otp.html',context)
def forgotpassword(request):
    if request.method=='POST':
        email = request.session.get('gmail')
        pass1=request.POST.get('pass1')
        password=request.POST.get('pass2')
        if pass1==password:
            edit=CustomUser.objects.get(email=email)
            hashed_password = make_password(password)  
            edit.password = hashed_password
            edit.save()
            key='3'
            messages.error(request, f'password successfully changed ({key})')
            return redirect('loginn')
        else:
            key='2'
            messages.error(request, f'passwords not matching ({key})')
            return redirect('forgotpassword')
    return render(request,'profile/forgotpassword.html')
def forgot(request):
    if request.method=='POST':
        email=request.POST.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            key='2'
            messages.error(request, f'This email address is not registered. ({key})')
            return redirect('forgot')
        else:
            user=CustomUser.objects.get(email=email)
            if user is not None:
                custom_user_manager = CustomUserManager()
                custom_user_manager.send_otp_email(request,email)
                return redirect('forgototp')
    return render(request,'profile/forgot.html')

def Resendotp(request):
    email=request.session.get('gmail')
    custom_user_manager = CustomUserManager()
    custom_user_manager.send_otp_email(request,email)
    return render(request,'userside/otp.html')

def resetpassword (request):
    if request.method =='POST':
        up = request.POST.get('password')
        np = request.POST.get('pass1')
        cp = request.POST.get('pass2')
        user = authenticate(request,password=up)
        if user is not None:
            if np == cp:
                edit = request.user
                hasedpassword = make_password(np)
                edit.password = hasedpassword
                edit.save()
                key='3'
                messages.error(request, f'password successfully changed ({key})')
                return redirect('profilehome')
    return render(request,'profile/resetpassword.html')
                

        
