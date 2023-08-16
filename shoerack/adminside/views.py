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
from cart.models import Order



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

# def product(request):
#     products = Product.objects.all()
#     category = Category.objects.all()
#     brand = Brand.objects.all()
   
        
#     return render(request,'admin_panel/product.html',{'products':products,'category':category,'brand':brand})


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

def Orders(request):
    ords=Order.objects.all()
    context={'ords':ords}
    return render(request,'admin_panel/ordermanagement.html',context)
def update_order_status(request,id):
    if request.method=='POST':
        st=request.POST.get('status')
        edit=Order.objects.get(id=id)
        edit.status=st
        edit.save()
        return redirect('ordermanagement')


