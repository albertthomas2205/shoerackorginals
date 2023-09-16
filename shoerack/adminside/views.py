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
from django.contrib.auth.decorators import login_required


@login_required(login_url='signin') 
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
    year_date = datetime.now(timezone.utc) - timedelta(days=365)
    today = datetime.now(timezone.utc) - timedelta(days=1)
    end_date = datetime.now(timezone.utc)
    weekly = Order.objects.filter(created_at__range=(week_date, end_date))
    monthly = Order.objects.filter(created_at__range=(month_date, end_date))
    yearly = Order.objects.filter(created_at__range=(year_date, end_date))
    daily = Order.objects.filter(created_at__range=(today, end_date))
    
    total_week_amount=0
    total_month_amount=0
    total_year_amount=0
    total_today_amount=0
    for dates in weekly:
        total_week_amount+=dates.total_price
    for dates in monthly:
        total_month_amount+=dates.total_price
    for dates in yearly:
        total_year_amount+=dates.total_price
    for dates in daily:
        total_today_amount+=dates.total_price
    context={'weekly':weekly,'monthly':monthly,'total_week_amount':total_week_amount,
             'total_month_amount':total_month_amount,'total_year_amount':total_year_amount,'total_today_amount':total_today_amount}
    
    return render(request, "admin_panel/index.html",context)

@login_required(login_url='signin') 
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


def sales_yearly(request):
    if request.method == 'POST':
        from_date_str = request.POST.get('from')
        to_date_str = request.POST.get('to')
        from_date = datetime.strptime(from_date_str, "%m/%d/%Y").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        to_date = datetime.strptime(to_date_str, "%m/%d/%Y").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else:
        # If no specific date range is provided, set a default range for the past year
        end_date = datetime.now(timezone.utc)
        from_date = (end_date - timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
        to_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

    # Filter orders created within the specified date range
    order = Order.objects.filter(created_at__range=(from_date, to_date))
    
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

def daily_sales(request):
    if request.method == 'POST':
        from_date_str = request.POST.get('from')
        to_date_str = request.POST.get('to')
        
        # Convert date strings to datetime objects
        from_date = datetime.strptime(from_date_str, "%m/%d/%Y")
        to_date = datetime.strptime(to_date_str, "%m/%d/%Y")
        
        # Set end_date to the end of the selected day
        end_date = to_date + timedelta(days=1, seconds=-1)
        
        # Query orders within the selected date range
        order = Order.objects.filter(created_at__range=(from_date, end_date))
    else:
        # If no date range is specified, show orders from the last day
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=1)
        order = Order.objects.filter(created_at__range=(start_date, end_date))
    
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


def sales_chart_daily(request):
    today = datetime.today()
    past_7_days = [today - timedelta(days=i) for i in range(20)]

    day_labels = [day.strftime('%Y-%m-%d') for day in past_7_days]
    sales_data = Order.objects.filter(created_at__date__in=[day.date() for day in past_7_days])

    daily_sales = []
    for day in past_7_days:
        x = sales_data.filter(created_at__date=day.date()).aggregate(total=Sum('total_price'))['total']
        day_sales = int(x) if x is not None else 0
        daily_sales.append(day_sales)
        print(x)
        name= 'Daily Report'
    context = {'name':name,'day_labels': day_labels, 'daily_sales': daily_sales}
    return render(request, 'admin_panel/chart.html', context)

def sales_chart_weekly(request):
    today = datetime.now(timezone.utc)
    past_weeks = [today - timedelta(weeks=i) for i in range(6, -1, -1)]

    labels = [week.strftime('%Y-%m-%d') for week in past_weeks]
    
    weekly_sales = []
    for week_start in past_weeks:
        week_end = week_start + timedelta(days=6)
        total_sales = Order.objects.filter(created_at__date__range=[week_start.date(), week_end.date()]).aggregate(total=Sum('total_price'))['total']
        week_sales = int(total_sales) if total_sales is not None else 0
        weekly_sales.append(week_sales)
        print(week_sales)

    context = {'name':'Weekly Report','day_labels': labels, 'daily_sales': weekly_sales}
    return render(request, 'admin_panel/chart.html', context)

def sales_chart_monthly(request):
    current_date = datetime.now(timezone.utc)
    current_year = current_date.year
    current_month = current_date.month

    monthly_sales = []
    labels = []

    for i in range(12, -1, -1):
        # Calculate the year and month for each past month
        year = current_year - (i // 12)
        month = (current_month - (i % 12)) % 12 or 12

        # Calculate the start and end dates for the current month
        month_start = datetime(year, month, 1, tzinfo=timezone.utc)
        month_end = (month_start + timedelta(days=32)).replace(day=1, microsecond=0, second=0, minute=0, hour=0) - timedelta(seconds=1)

        labels.append(month_start.strftime('%Y-%m-%d'))

        # Calculate the total sales for the current month
        total_sales = Order.objects.filter(created_at__range=(month_start, month_end)).aggregate(total=Sum('total_price'))['total']
        month_sales = int(total_sales) if total_sales is not None else 0
        monthly_sales.append(month_sales)

    context = {'name': 'Monthly Report', 'day_labels': labels, 'daily_sales': monthly_sales}
    return render(request, 'admin_panel/chart.html', context)




def signinn(request):
    return render(request,'account/signin.html')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url='signin') 
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

      
@login_required(login_url='signin')  
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





@login_required(login_url='signin') 
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


def deactivatecoupon(request, id):
    coup = Coupon.objects.get(id=id)
    if coup.active == True:
        coup.active = False
        coup.save()
    else:
        coup.active = True
        coup.save()
        
    return redirect("admincoupon")
def deletecoupon(request,id):
    coup = Coupon.objects.get(id = id)
    coup.delete()
    
    return redirect("admincoupon")
    



@login_required(login_url='signin') 
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

@login_required(login_url='signin') 
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
        
       
        images = request.FILES.getlist('images')
        for image in images:
                ProductImage.objects.create(product=product, image=image)
        print(images,brand)
        product.save()
        return redirect('product')
    category = Category.objects.all()
    brand = Brand.objects.all()
    contex= {'category':category,'brand':brand}
    return render(request,'admin_panel/product.html',contex)





@login_required(login_url='signin') 
def productsizee(request,id):
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
        return redirect('productsizee',id) 
    
    return render(request,'admin_panel/productsize.html',context)


@login_required(login_url='signin') 
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
        
        return redirect('product')
    
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
 
@login_required(login_url='signin')   
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
    k = 150
    sub_price -=k
    total_price = order.total_price+k
    print(total_price)
    context = {
        "order_items": order_items,
        "order": order,
        "sub_price": sub_price,
        "address": address,
        'total_price':total_price
    }
    return render(request, "admin_panel/uniqueorder.html", context)

def order_cancel(request, id):
    edit = OrderItem.objects.get(id=id)
    edit.status = "C"
    edit.save()
    id = edit.order.id
    return redirect("adminorder_deatails", id)

    

def update_order_status(request, id):
    if request.method == "POST":
        st = request.POST.get("status")
        edit = OrderItem.objects.get(id=id)
        edit.status = st
        edit.save()
        id = edit.order.id
        print(edit.order.address.custom_name)
      
        return redirect("adminorder_deatails", id)



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
    



