from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from user.models import CustomUser
from .models import Category,Product,ProductImage,Brand
from django.shortcuts import render, redirect
from .models import Category
from .forms import ProductForm, ProductImageForm,Productsize,ProductsizeForm
from account.models import Order,OrderItem,Userdetails
from decimal import Decimal
from datetime import datetime
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from cart.models import Coupon
from account.models import OrderReturn,Wallet,Wallethistory
from datetime import  date, datetime, timedelta, timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.core.serializers import serialize
import json
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncYear, TruncWeek
from django.http import JsonResponse
\
def AdminDashboard(request):
    if request.method=='POST':
        from_date_str=request.POST.get('from')
        To_date_str=request.POST.get('to')
        from_date = datetime.strptime(from_date_str, "%m/%d/%Y").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        to_date = datetime.strptime(To_date_str, "%m/%d/%Y").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else: 
        from_date = None
        to_date = None
    week_date = datetime.now(timezone.utc) - timedelta(days=7) 
    month_date = datetime.now(timezone.utc) - timedelta(days=30)
    end_date = datetime.now(timezone.utc)
    weekly = Order.objects.filter(created_at__range=(week_date, end_date))
    monthly = Order.objects.filter(created_at__range=(month_date, end_date))
    total_week_amount=0
    total_month_amount=0
    for dates in weekly:
        total_week_amount+=dates.total_price
    for dates in monthly:
        total_month_amount+=dates.total_price
   
    context={'weekly':weekly,'monthly':monthly,'total_week_amount':total_week_amount,'total_month_amount':total_month_amount}
    
    return render(request, "admin_panel/index.html",context)

def chart(request):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    monthly_sales = Order.objects.filter(created_at__range=(start_date, end_date)) \
        .annotate(month=TruncMonth('created_at')) \
        .values('month') \
        .annotate(total_sales=Sum('total_price')) \
        .order_by('month')

    # sales = OrderItem.objects.exclude(order_status_choices='Cancelled')
    monthly_sales_list = list(monthly_sales)
    monthly_sales_json = json.dumps(monthly_sales_list, default=str)
    context = {
        'monthly_sales': monthly_sales_json,
        # 'sales': sales,
    }

    return render(request, 'admin_panel/chart.html', context)

def yearly(request):
    yearly_order_data = Order.objects.annotate(year=TruncYear('created_at')).values(
        'year').annotate(order_count=Count('id')).order_by('year')
    labels = [item['year'].strftime('%Y') for item in yearly_order_data]
    data = [item['order_count'] for item in yearly_order_data]
    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'admin/yearly_chart.html', context)

def monthly(request):
    monthly_order_data = Order.objects.annotate(month=TruncMonth('order_date')).values(
        'month').annotate(order_count=Count('id')).order_by('month')
    labels = [item['month'].strftime('%Y-%m') for item in monthly_order_data]
    data = [item['order_count'] for item in monthly_order_data]
    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'admin/monthly_chart.html', context)

def sales_report(request):
    if request.method=='POST':
        from_date_str=request.POST.get('from')
        To_date_str=request.POST.get('to')
        end_date = datetime.now(timezone.utc)
        from_date = datetime.strptime(from_date_str, "%m/%d/%Y").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        to_date = datetime.strptime(To_date_str, "%m/%d/%Y").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else: 
        from_date = None
        to_date = None
    end_date = datetime.now(timezone.utc)
    week_date = datetime.now(timezone.utc) - timedelta(days=7) 
    order = Order.objects.filter(created_at__range=(week_date, end_date))
    items = []
    
    for ord in order:
        item = OrderItem.objects.filter(order=ord)
        
        for ite in item:
            items.append(ite)
    context = {
        'order': order,
        'items': items
    }
    return render(request, 'admin_panel/sales_report.html', context)


def sales_monthly(request):
    if request.method=='POST':
        from_date_str=request.POST.get('from')
        To_date_str=request.POST.get('to')
        end_date = datetime.now(timezone.utc)
        from_date = datetime.strptime(from_date_str, "%m/%d/%Y").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        to_date = datetime.strptime(To_date_str, "%m/%d/%Y").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else: 
        from_date = None
        to_date = None
    end_date = datetime.now(timezone.utc)
    month_date = datetime.now(timezone.utc) - timedelta(days=30)
    order = Order.objects.filter(created_at__range=(month_date, end_date))
    items = []
    
    for ord in order:
        item = OrderItem.objects.filter(order=ord)
        
        for ite in item:
            items.append(ite)
    context = {
        'order': order,
        'items': items
    }
    return render(request, 'admin_panel/sales_report.html', context)


from datetime import datetime


def sales_daily(request):
    if request.method == 'POST':
        from_date_str = request.POST.get('fromDate')
        to_date_str = request.POST.get('toDate')
        
        # Parse the date strings using the correct format ('%Y-%m-%d')
       
        from_date = datetime.strptime(from_date_str, "%Y-%m-%d").strftime(
             "%Y-%m-%d %H:%M:%S"
        )
        to_date = datetime.strptime(to_date_str, "%Y-%m-%d").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else: 
        from_date = None
        to_date = None
        
    # Query the database to get orders within the specified date range
    orders = Order.objects.filter(created_at__range=(from_date, to_date))
    
    # Retrieve all related items for the selected orders
    items = OrderItem.objects.filter(order__in=orders)
    
    context = {
        'order': orders,
        'items': items
    }
    
    return render(request, 'admin_panel/sales_report.html', context)



def signinn(request):
    return render(request,'account/signin.html')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def user(request):
    data = CustomUser.objects.all()
    
    # Set the number of users per page
    users_per_page = 2 # You can adjust this number as needed

    paginator = Paginator(data, users_per_page)
    page_number = request.GET.get('page')

    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    context = {
        'data': paginated_data,
    }
    
    return render(request, 'admin_panel/userdetails.html', context)


def signin(request):

    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        user=authenticate(request, email=email,password=password)
        if user is not None and user.is_superuser:
            login(request,user)
            return redirect('adminhome')
        else:
         
            messages.error(request, "Invalid credentials")
    return render(request,'admin_panel/signin.html')

    
def adminhome(request):
    
    return render(request,'admin_panel/index.html')


def block_user_view(request,id):
   
    if request.method == 'POST':
       
            
        user = CustomUser.objects.get(id=id)
        if user.is_active:
            
            user.is_active = False
        else:
            user.is_active=True
        user.save()

    return redirect('user')


def base(request):
    return render(request,'admin_panel/base.html')




def product(request):
    products = Product.objects.all()
    category = Category.objects.all()
    brand = Brand.objects.all()

    # Number of items to display per page
    items_per_page = 5# You can adjust this number as needed

    paginator = Paginator(products, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the requested page number
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_panel/product.html', {
        'products': page_obj,
        'category': category,
        'brand': brand,
    })
def signout(request):
    logout(request)
    return redirect('signin')

def category(request):
    if request.method == 'POST':
        categoryname = request.POST.get('category')
        if Category.objects.filter(category_name = categoryname).exists():
            messages.error(request,'category already exists')
        else:
            category = Category(category_name=categoryname)
            category.save()

            
        
    brand = Brand.objects.all()   
    categories = Category.objects.all()
  
    
    return render(request,'admin_panel/category.html',{'categories':categories,'brand':brand})

def addbrand(request):
    if request.method == 'POST':
        brandname = request.POST.get('brandname')
        if Brand.objects.filter(brand_name=brandname).exists():
           messages.error(request,('This brand  already exists'))
           return redirect('addbrand')
        else:
            brand= Brand(brand_name = brandname)
            brand.save()
        return redirect('category')  

def addproduct(request):
    if request.method == 'POST':
        productname = request.POST.get('name')
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')
        color = request.POST.get('color')
        category = get_object_or_404(Category,id = category_id)
        brand = get_object_or_404(Brand,id = brand_id)
        product = Product.objects.create(name=productname,category=category,brand = brand,color=color)
        
       
        images = request.FILES.getlist('image')
        for image in images:
                ProductImage.objects.create(product=product, image=image)
        product.save()
        return redirect('product')
    category = Category.objects.all()
    brand = Brand.objects.all()
    contex= {'category':category,'brand':brand}
    return render(request,'admin_panel/product.html',contex)





def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        image_form = ProductImageForm(request.POST, request.FILES)
        if product_form.is_valid() and image_form.is_valid():
            product = product_form.save()
            images = request.FILES.getlist('image')
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            return redirect('product_list')  # Replace 'product_list' with the URL name for the product list page
    else:
        product_form = ProductForm()
        image_form = ProductImageForm()

    # Get the available categories and subcategories from the database
    categories = Category.objects.all()
    brands = Brand.objects.all()

    return render(request, 'admin_panel/add_product.html', {
        'product_form': product_form,
        'image_form': image_form,
        'categories': categories,
        'brands': brands,
    })


def productsize(request,id):
    product= get_object_or_404(Product,id=id)
    var = Productsize.objects.filter(product = product)
    context = {'var':var}
   
    if request.method== 'POST':
        description = request.POST.get('description')
        size = request.POST.get('size')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        productsize = Productsize.objects.create(product=product,description= description,size=size,stock=stock,price= price)
        productsize.save() 
        return redirect('productsize',id) 
    
    return render(request,'admin_panel/productsize.html',context)


def editproductsize(request, id):
    product_size = get_object_or_404(Productsize, id=id)
    
    if request.method == 'POST':
        description = request.POST.get('description')
        size = request.POST.get('size')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        
        # Update the product size details
        product_size.description = description
        product_size.size = size
        product_size.stock = stock
        product_size.price = price
        product_size.save()
        
        return redirect('productsize', id=product_size.product.id)
    
    context = {'product_size': product_size}
    return render(request, 'admin_panel/varientedit.html', context)



def delete_product_size(request, id):
    product_size = get_object_or_404(Productsize, id=id)
    k = product_size.product.id
    product_size.delete()
    messages.success(request, 'Product size deleted successfully.')
    return redirect('productsize', id=k)

  

def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    product_images = ProductImage.objects.all()  # Fetch all product images from the database
    context = {
        'products': products,
        
    }
    return render(request, 'admin_panel/product_list.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Category

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        # Process the form data submitted for editing
        category_name = request.POST['category_name']
        # Update the category object
        category.category_name = category_name
        category.save()
        return redirect('category')  # Replace 'category_list' with the URL name of the page displaying the category list

    # Render the template for editing the category
    return render(request, 'admin_panel/category.html', {'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        # Delete the category
        category.delete()
        return redirect('category')  # Replace 'category_list' with the URL name of the page displaying the category list
    category = Category.objects.all()
    brand = Brand.objects.all()
    contex= {'category':category,'brand':brand}
    # Render the template for confirming category deletion
    return render(request, 'admin_panel/category.html',contex)

def delete_product (request, id):
    product = get_object_or_404(Product,id = id)
    if request.method == 'POST':
            
        product.delete()
        return redirect('product')
    



# def Orders(request):
    
#     all_orders = Order.objects.all()
#     per_page = 3
#     paginator = Paginator(all_orders, per_page)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'page_obj': page_obj,
#     }

#     return render(request, 'admin_panel/ordermanagement.html', context)
def Orders(request):
    orders = Order.objects.all().order_by("-created_at")
    paginator = Paginator(orders, per_page=3)

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "orders": page,
    }
    return render(request, "admin_panel/ordermanagement.html", context)
def adminorder_deatails(request, id):
    order = Order.objects.get(id=id)
    order_items = OrderItem.objects.filter(order=order)
    try:
        x = Decimal(order.coupon_applied.discount)
        sub_price = order.total_price + x
    except:
        sub_price = order.total_price
    address = Userdetails.objects.get(id=order.address.id)
    context = {
        "order_items": order_items,
        "order": order,
        "sub_price": sub_price,
        "address": address,
    }
    return render(request, "admin_panel/uniqueorder.html", context)

def order_cancel(request, id):
    edit = OrderItem.objects.get(id=id)
    edit.status = "C"
    edit.save()
    id = edit.order.id
    return redirect("adminorder_deatails", id)

# def update_order_status(request,id):
#     if request.method=='POST':
#         st=request.POST.get('status')
#         edit=Order.objects.get(id=id)
#         edit.status=st
#         edit.save()
#         return redirect('ordermanagement')
    

def update_order_status(request, id):
    if request.method == "POST":
        st = request.POST.get("status")
        edit = OrderItem.objects.get(id=id)
        edit.status = st
        edit.save()
        id = edit.order.id
        print(edit.order.address.custom_name)
      
        return redirect("adminorder_deatails", id)


    
    


# def Admincoupon(request):
#     if request.method == "POST":
#         code = request.POST.get("code")
#         discount = request.POST.get("discount")
#         minamount = request.POST.get("minamount")
#         valid_from_str = request.POST.get("from")
#         valid_to_str = request.POST.get("to")
#         valid_from = datetime.strptime(valid_from_str, "%m/%d/%Y").strftime(
#             "%Y-%m-%d %H:%M:%S"
#         )
#         valid_to = datetime.strptime(valid_to_str, "%m/%d/%Y").strftime(
#             "%Y-%m-%d %H:%M:%S"
#         )
#         Coupon.objects.create(
#             code=code,
#             minimumamount=minamount,
#             discount=discount,
#             valid_from=valid_from,
#             valid_to=valid_to,
#         )
#         return redirect("admincoupon")
#     datas = Coupon.objects.all()
#     return render(request, "admin_panel/coupons.html", {"datas": datas})


def Admincoupon(request):
    if request.method == "POST":
        try:
            code = request.POST.get("code")
            discount = request.POST.get("discount")
            minamount = request.POST.get("minamount")
            valid_from_str = request.POST.get("from")
            valid_to_str = request.POST.get("to")
            
            valid_from = datetime.strptime(valid_from_str, "%d/%m/%Y").strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            valid_to = datetime.strptime(valid_to_str, "%d/%m/%Y").strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            
            Coupon.objects.create(
                code=code,
                minimumamount=minamount,
                discount=discount,
                valid_from=valid_from,
                valid_to=valid_to,
            )
            return redirect("admincoupon")
        except ValueError:
            error_message = "Invalid date format. Please use the format dd/mm/yyyy."
            datas = Coupon.objects.all()
            return render(request, "admin_panel/coupons.html", {"datas": datas, "error_message": error_message})
    datas = Coupon.objects.all()
    return render(request, "admin_panel/coupons.html", {"datas": datas})



def Returns(request):
    returns = OrderReturn.objects.all().order_by('-created_at')
    paginator = Paginator(returns, per_page=3)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {'returns': page}
    return render(request,'admin_panel/return.html', context)


def returndetails(request,id):
    item = OrderReturn.objects.get(id=id)
    context = {'item':item}
    return render(request,'admin_panel/returndetails.html', context)

def update_return_status(request,id):
    if request.method == "POST":
        st = request.POST.get("status")
        edit = OrderReturn.objects.get(id=id)
        edit.status = st
        edit.save()
        tt = edit.total_price
     
            
        if edit.status == 'R':
            try:
                 wallet = Wallet.objects.get(user=edit.user)
            except:
                wallet = Wallet.objects.create(user= edit.user)
            wallet = Wallet.objects.get(user=edit.user)
            total_coins=wallet.coins
            total_coins += tt
            wallet.coins = total_coins
            wallet.save()
            Wallethistory.objects.create(task=f"Product return {edit.orderitem.product.product.name}",wallet=wallet,coins=edit.total_price)
        return redirect('returndetails',id)
    



