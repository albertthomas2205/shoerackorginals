from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,validators
from .models import CustomUserManager
from django.contrib.sessions.models import Session
from adminside.models import Product,ProductImage,Category,Productsize,Brand
from account.models import Userdetails
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helpers import send_otp_phone
from .models import CustomUser
from cart.models import CartItem


# # Create your views here.
def index(request):
    products = Product.objects.all()
    category = Category.objects.all()
    count = CartItem.objects.all().count()

            
    return render(request,'userside/index.html',{'products':products,'category':category,'cart_item_count':count})



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


# def product_detail_view(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     relatedproducts = Product.objects.filter(id = product_id)
#     k=ProductImage.objects.filter(product=product)
#     context = {'product': product,'k':k,'products':relatedproducts}
#     return render(request, 'userside/singleproduct.html',context)

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Get the brand of the current product
    current_brand = product.brand
    
    # Filter related products by brand and exclude the current product
    relatedproducts = Product.objects.filter(brand=current_brand).exclude(pk=product_id)
    
    # Retrieve product images
    k = ProductImage.objects.filter(product=product)
    
    context = {'product': product, 'k': k, 'products': relatedproducts}
    return render(request, 'userside/singleproduct.html', context)

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



def category(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    name = category.category_name
    
    # Set the number of products per page
    products_per_page = 4 # You can adjust this number as needed

    paginator = Paginator(products, products_per_page)
    page_number = request.GET.get('page')

    try:
        paginated_products = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    context = {
        'category': name,
        'paginated_products': paginated_products,
    }
    return render(request, 'userside/category.html', context)

    
from account.models import Userdetails
from adminside.forms import UserdetailsForm  # Create a Django form for Userdetails

def shop(request):
    products = Product.objects.all()
    name = 'Shop'
    
    # Set the number of products per page
    products_per_page = 4  # You can adjust this number as needed

    paginator = Paginator(products, products_per_page)
    page_number = request.GET.get('page')

    try:
        paginated_products = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    context = {
        'paginated_products': paginated_products,
        'category': name,
    }
    return render(request, 'userside/category.html', context)




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



def search(request):
    if request.method == 'POST':
        result = request.POST.get('search')
        result1 = request.POST.get('search')
        result2 = request.POST.get('search')
        try:
            product = Product.objects.filter(name__icontains=result)
            brand = Brand.objects.filter(brand_name__icontains= result1)
            
            category = Category.objects.filter(category_name__istartswith=result2)
        except:
             product = []
             brand = []
             category = []
            
             # Handle any other exceptions that might occur
          
        return render(request, 'userside/search.html', {'product':product,'brand':brand,'category':category} )
    return render(request, 'userside/search.html', {})

@api_view(['POST'])
def send_otp(request):
    data = request.data
    
    if data.get('phone_number') is None:
        return Response({
            'status':400,
            'message': 'Key phone number is required'
        })
    if data.get('password') is None:
        return Response({
            'status':400,
            'message':'key phone_number is required'
        })
    user  = CustomUser.objects.create(
        phone_number = data.get('phone_number'),
        otp = send_otp_phone(data.get('phone_number'))
        )
    user.set_password = data.get('set_password')
    user.save()
    
    return Response({
        'status':200,
        'message': 'Otp sent'
        
    })
    
@api_view(['POST'])
def verify_otp(request):
    data = request.data
    
    if data.get('phone_number') is None:
        return Response({
            'status':400,
            'message': 'Key phone number is required'
        })
    if data.get('otp') is None:
        return Response({
            'status':400,
            'message':'key otp is required'
        })
    try :
        user_obj = CustomUser.objects.get(phone_number =data.get('phone_number'))
    
    except Exception as e:
        return Response({
            'status':400,
            'message':'invalid phone'
        })
    if user_obj.otp == data.get('otp'):
        return Response({
            'status':200,
            'message': 'otp matched'
        })
    return Response({
        'status':400,
        'message': 'invalid otp'
    })
    




