from django.shortcuts import render,redirect,get_object_or_404
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,validators
from .models import CustomUserManager
from django.contrib.sessions.models import Session
from adminside.models import Product,ProductImage,Category,Productsize
from user.models import Userdetails
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    products = Product.objects.all()
    category = Category.objects.all()
            
    return render(request,'userside/index.html',{'products':products,'category':category})



def register(request):
    if request.user.is_authenticated:
            return redirect('indexx.html')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if pass1 == pass2 and len(pass1) > 4 and pass1 != name:
            
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect('register')
            else:
                custom_user_manager = CustomUserManager()
                custom_user_manager.send_otp_email(request,email)
                myuser = CustomUser.objects.create_user(name=name, email=email,phone_number=phone_number,password = pass1)
                myuser.save()

                return redirect('otp')
        
        else:
            messages.error(request, "please check yor password")
            return redirect('register')
    
    return render(request, 'userside/register.html')



def loginn(request):
    if request.user.is_authenticated:
            return redirect('index')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        user=authenticate(request,email=email,password=password)
        if user is not None:
            print('haiiiiii')
            custom_user_manager = CustomUserManager()
            custom_user_manager.send_otp_email(request,email)
            login(request,user)
            return redirect('otp')
        else:
            print('user is none')
            messages.error(request, "Invalid password/email")
            return redirect('loginn')
       
    return render(request,'userside/login.html')


def signoutt(request):
    logout(request)
    return redirect('index')
   

def otpp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
     
        if user_otp == stored_otp:
           
            return redirect('index')
        else:
            return redirect('otp')
  
    return render(request,'userside/otp.html')

from adminside.models import Product

def productsample(request):
    products = Product.objects.all()
    return render(request, 'userside/productsample.html', {'products': products})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    k=ProductImage.objects.filter(product=product)
    context = {'product': product,'k':k}
    return render(request, 'userside/singleproduct.html',context)

from django.http import JsonResponse


def update_price(request):
    if request.method == 'GET':
        product_id = request.GET.get('product')
        selected_size = request.GET.get('size')
        try:
            product = Product.objects.get(pk=product_id)
            product_size = Productsize.objects.get(product=product, size=selected_size)
            return JsonResponse({'price': str(product_size.price)})
        except (Product.DoesNotExist, Productsize.DoesNotExist):
            return JsonResponse({'error': 'Product or size not found'}, status=400)


def base(request):
    return render(request,'userside/sigle.html')


@login_required
def addaddress(request):
    user = request.user
    # Now 'user' contains the currently logged-in user object.
    return render(request, 'userside/address.html')

def category(request,id):
    category = get_object_or_404(Category,id=id)
  
    product = Product.objects.filter(category=category)
    context = {'product':product}
    return render(request,'userside/category.html',context)
    
from .models import Userdetails
from adminside.forms import UserdetailsForm  # Create a Django form for Userdetails

def shop(request):
    shop = Product.objects.all()
    context = {'shop':shop}
    return render(request,'userside/category.html',context)



def profilebase(request):
    return render(request,'userside/profilebase.html')

@login_required
def user_details(request):
    # Retrieve the logged-in user's details
    addresses = Userdetails.objects.filter(userr=request.user)
    print('haiiii')
    print(addresses)

    # Pass the user_details object to the HTML template
    return render(request, 'userside/profile.html', {'addresses': addresses})


def add_address(request):
    if request.method == 'POST':
        form = UserdetailsForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.userr = request.user  # Assuming you have a CustomUser model and using request.user for the logged-in user
            address.save()
            return redirect('details')  # Replace 'address_list' with the URL name of the page displaying the list of addresses
    else:
        form = UserdetailsForm()
    
    return render(request, 'userside/address.html', {'form': form})

def edit_address(request, address_id):
    address = get_object_or_404(Userdetails, id=address_id)

    if request.method == 'POST':
        form = UserdetailsForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('address_list')  # Replace 'address_list' with the URL name of the page displaying the list of addresses
    else:
        form = UserdetailsForm(instance=address)

    return render(request, 'edit_address.html', {'form': form, 'address': address})

def edit_address(request, userdetails_id):
    userdetails = get_object_or_404(Userdetails, id=userdetails_id)

    if request.method == 'POST':
        form = UserdetailsForm(request.POST, instance=userdetails)
        if form.is_valid():
            form.save()
            return redirect('user_addresses')  # Replace with the URL name for success
    else:
        form = UserdetailsForm(instance=userdetails)

    context = {'form': form}
    return render(request, 'userside/address.html', context)

def delete_address(request, userdetails_id):
    userdetails = get_object_or_404(Userdetails, id=userdetails_id)
    
    if request.method == 'POST':
        userdetails.delete()
        return redirect('user_adddresses')  # Replace with the URL name for success

    return redirect('userside/profile.html', userdetails_id=userdetails_id)



