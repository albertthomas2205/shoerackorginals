from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from user.models import CustomUser
from .models import Category,Subcategory,Product,ProductImage
from django.shortcuts import render, redirect
from .models import Category, Subcategory



def signinn(request):
    return render(request,'account/signin.html')

def user(request):
    data = CustomUser.objects.all()
    context={"data":data}
    return render(request,'admin_panel/userdetails.html',context)
    

def signin(request):
    # if request.user.is_authenticated:
    #         return redirect('adminhome')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        user=authenticate(request, email=email,password=password)
        if user is not None and user.is_superuser:
            print('haiii')
            # custom_user_manager = CustomUserManager()
            # custom_user_manager.send_otp_email(request,email)
            login(request,user)
            return redirect('adminhome')
        else:
            print("hellowwww")
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
    return render(request,'admin_panel/product.html',{'products':products})

def signout(request):
    logout(request)
    return redirect('signin')

def category(request):
    categories = Category.objects.all()
    return render(request,'admin_panel/category.html',{'categories': categories})

def add_category(request):
    if request.method == 'POST':
        
        category_name = request.POST.get('category_name')
        category = Category(name=category_name)
        category.save()
        
        return redirect('category')  

    return render(request, 'admin_panel/add_category.html')


def edit_category(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        edit = Subcategory.objects.get(id=id)
        edit.name = name
        edit.save()
        return redirect('category')
    return render(request, 'admin_panel/edit_category.html')

def delete_category(request, name):
    category = get_object_or_404(Category, name=name)
    if request.method == 'POST':
        category.delete()
        return redirect('category')
    return redirect('category')


def delete_sub(request, name):
    category = get_object_or_404(Subcategory, name=name)
    if request.method == 'POST':
        category.delete()
        return redirect('category')
    return redirect('category')

def add_sub(request):
    if request.method == 'POST':
        
        category_name = request.POST.get('category_name')
        category = Subcategory(name=category_name)
        category.save()
        
        return redirect('sub')  

    return render(request, 'admin_panel/add_sub.html')

def edit_sub(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        edit = Subcategory.objects.get(id=id)
        edit.name = name
        edit.save()
        return redirect('category')
    return render(request, 'admin_panel/edit_category.html')

 



def delete_sub(request, name):
    category = get_object_or_404(Category, name=name)
    if request.method == 'POST':
        category.delete()
        return redirect('sub')
    return redirect('sub')




def sub(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    return render(request, 'admin_panel/sub.html', {'categories': categories, 'subcategories': subcategories})
    

def create_subcategory(category_instance, subcategory_name):
    # Create and save a new Subcategory instance
    subcategory = Subcategory.objects.create(category=category_instance, name=subcategory_name)
    return subcategory

def add_subvb(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        subcategory_name = request.POST.get('subcategory_name')

        # Get the Category instance using the selected category_id
        try:
            category_instance = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            # Handle the case where the category_id does not exist
            # You may redirect back to the form with an error message, etc.
            return render(request, 'add_subc.html', {'categories': Category.objects.all()})

        # Call the function to create and save a new Subcategory instance
        create_subcategory(category_instance, subcategory_name)

        # Redirect to a page or URL after successfully adding the subcategory
        return redirect('sub')  # Replace 'sub' with the appropriate URL name for the subcategory listing

    return render(request, 'admin_panel/add_sub.html', {'categories': Category.objects.all()})


# views.py

from .forms import ProductForm


    
# In your app's views.py file
from django.shortcuts import render, redirect
from .models import Product, Category, Subcategory

def edit_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        # Handle the case when the product doesn't exist
        return redirect('product_list')  # Redirect to the product list page or an error page

    if request.method == 'POST':
        # Handle the form submission for editing the product here
        # You can update the product details based on the submitted form data
        product.name = request.POST.get('name')
        product.stock = request.POST.get('stock')
        product.color = request.POST.get('color')
        product.size = request.POST.get('size')
        product.price = request.POST.get('price')
        product.category_id = request.POST.get('category')
        product.subcategory_id = request.POST.get('subcategory')
        product.save()
        return redirect('product_list')  # Redirect to the product list page after successful edit

    # If the request method is GET, display the edit form
    # Pass the product instance, categories, and subcategories to the template for pre-populating the form
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(request, 'admin_panel/edit_product.html', context)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return redirect('product_list')

def delete_sub(request,subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    if request.method == 'POST':
        subcategory.delete()
        return redirect('sub')
    return redirect('sub')



from django.shortcuts import render, redirect
from .models import Category, Subcategory

def add_sub(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('subcategory_name')

        category = Category.objects.get(pk=category_id)
        Subcategory.objects.create(category=category, name=name)

        return redirect('sub')  # Redirect to the same page after adding subcategory

    else:
        categories = Category.objects.all()
        return render(request, 'admin_panel/add_sub.html', {'categories': categories})
from django.shortcuts import render, redirect
from .forms import ProductForm, ProductImageForm
from .models import Category, Subcategory

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
    subcategories = Subcategory.objects.all()

    return render(request, 'admin_panel/add_product.html', {
        'product_form': product_form,
        'image_form': image_form,
        'categories': categories,
        'subcategories': subcategories
    })

# views.py

from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    product_images = ProductImage.objects.all()  # Fetch all product images from the database
    context = {
        'products': products,
        
    }
    return render(request, 'admin_panel/product_list.html', context)

# views.py

from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product

# def edit_product(request, product_id=None):
#     if product_id:
#         # Edit existing product
#         product = Product.objects.get(id=product_id)
#     else:
#         # Add new product
#         product = None

#     if request.method == 'POST':
#         form = ProductForm(request.POST, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('admin_panel/product_list')  # Redirect to the product list page
#     else:
#         form = ProductForm(instance=product)

#     return render(request, 'admin_panel/edit_product.html', {'form': form})

