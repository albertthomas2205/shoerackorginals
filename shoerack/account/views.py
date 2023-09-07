from django.shortcuts import render, HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from adminside.forms import UserdetailsForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from user.models import CustomUser,CustomUserManager
from account.models import Userdetails,Wallethistory,Wallet
from account.models import Order,OrderItem,OrderReturn
from django.contrib.auth import authenticate
from decimal import Decimal
from datetime import datetime

    

def profilehome(request):
    addresses= request.user
  
        
    try:    
        wallet=Wallet.objects.get(user=request.user)
        wallethistory=Wallethistory.objects.filter(wallet=wallet).order_by('-created_at')
    
    except:
        
            wallet=Wallet.objects.create(user=request.user)
            wallethistory=None
    email = request.user.email
    parts = email.split("@")
    if len(parts) == 2:
        code = parts[0]
        print(f"Username: {code}")
    else:
        print("Invalid email address format")
        
  
    return render(request,'profile/profilehome.html',{'addresses':addresses ,'wallet':wallet,'wallethistory':wallethistory,'code':code})
# def edit_category(request, category_id):
#     category = get_object_or_404(Category, id=category_id)

#     if request.method == 'POST':
#         # Process the form data submitted for editing
#         category_name = request.POST['category_name']
#         # Update the category object
#         category.category_name = category_name
#         category.save()
#         return redirect('category')  # Replace 'category_list' with the URL name of the page displaying the category list

#     # Render the template for editing the category
#     return render(request, 'admin_panel/category.html', {'category': category})


def edit_profile(request,id):
    id = get_object_or_404(CustomUser,id=id)
    print(id.name)
    if request.method == 'POST':
        newname= request.POST.get('name')
        id.name = newname
        id.save()
        return redirect('profilehome')
    wallet=Wallet.objects.get(user=request.user)
    wallethistory=Wallethistory.objects.filter(wallet=wallet).order_by('-created_at')
    addresses= request.user
    return render(request,'profile/profilehome.html',{'addresses':addresses ,'wallet':wallet,'wallethistory':wallethistory})
    


def viewaddress(request):
    # Retrieve the logged-in user's details
    addresses = Userdetails.objects.filter(userr=request.user)
    # Pass the user_details object to the HTML template
    return render(request, 'profile/viewadddress.html', {'addresses': addresses,})

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


from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator




def userorders(request):
    cust = get_object_or_404(CustomUser, id=request.user.id)
    orders = Order.objects.filter(user=cust).order_by('-created_at')

    # Number of items to show per page
    items_per_page = 3 # You can adjust this number as per your preference

    paginator = Paginator(orders, items_per_page)
    
    page_number = request.GET.get('page')
    page_orders = paginator.get_page(page_number)
    
    context = {'page_orders': page_orders, 'cust': cust}
    return render(request, 'profile/orders.html', context)

def order_deatails(request,id):
    order=Order.objects.get(id=id)
    order_items=OrderItem.objects.filter(order=order)
    try:
        x=Decimal(order.coupon_applied.discount)
        sub_price = order.total_price + x
    except:
        sub_price = order.total_price
    k = 150
    total = order.total_price+k
    address=Userdetails.objects.get(id=order.address.id)
    context={'order_items':order_items,'order':order,'sub_price':sub_price,'address':address,'total':total}
    return render(request, 'profile/orderitems.html',context)



def Usercancel(request,id):
    edit=get_object_or_404(OrderItem,id=id)
    edit.status='C'
    edit.save()
    return redirect('userorders')


    
def userorder_cancel(request,id):
    edit=OrderItem.objects.get(id=id)
    edit.status='C'
    edit.save()
    tt = edit.total_itemprice
    wallet = Wallet.objects.get(user=request.user)
    total_coins=wallet.coins
    total_coins += tt
    wallet.coins = total_coins 
    wallet.save()
    Wallethistory.objects.create(task=f"Product cancel {edit.product.product.name}",wallet=wallet,coins=edit.total_itemprice)
    id = edit.order.id
    return redirect('order_deatails',id)

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
        hased = make_password(up)
        k = get_object_or_404(CustomUser,email=request.user.email)
        h = authenticate(request,email=k.email,password=up)
        if k.password == hased:
            print('bibin')
       
        np = request.POST.get('pass1')
        cp = request.POST.get('pass2')
        
        if h is not None:
            print('haiiiiii')
            if np == cp:
                edit = request.user
                hasedpassword = make_password(np)
                edit.password = hasedpassword
                edit.save()
                key='3'
                messages.error(request, f'password successfully changed ({key})')
                return redirect('loginn')
    return render(request,'profile/resetpassword.html')

# for generating pdf invoice
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
                
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def product_return(request,id):
    orderitem=OrderItem.objects.get(id=id)
    orderitem.returnstatus = True
    orderitem.save()
    try:
        c = orderitem.order.coupon_applied
        order = OrderItem.objects.filter(order=orderitem.order)
        count = order.count()
        k = 150
        first = c.discount//count
        fi = Decimal(first)
        total_price= orderitem.total_itemprice - fi + k
        print(total_price)
    except:
        k = 15
        total_price =orderitem.total_itemprice + k
    finally:
        OrderReturn.objects.create(orderitem=orderitem,user=request.user,total_price=total_price)
        id = orderitem.order.id
    return redirect('order_deatails',id)



def render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="tails invoice.pdf"'

    pisa_status = pisa.CreatePDF(
        html, dest=response
    )

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def generate_invoice(request,id):
    order = Order.objects.get(id=id)
    orderitems = OrderItem.objects.filter(order = order)
    if order.coupon_applied:
        t = order.total_price
        c = order.coupon_applied.discount
        c = Decimal(c)
        k = 150
        total = t + c+ k
        print(total)
    else:
        total = order.total_price
    context = {'order':order,'orderitems':orderitems ,'total':total}
    pdf = render_to_pdf('profile/invoice.html', context)

    # Set content type and headers for download
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response




        
