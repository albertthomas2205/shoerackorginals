from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from user.models import CustomUser
from .models import Category,Subcategory
from django.shortcuts import render, redirect
from .models import Category, Subcategory



def signinn(request):
    return render(request,'account/signin.html')

def user(request):
    data = CustomUser.objects.all()
    context={"data":data}
    return render(request,'admin_panel/sample-page.html',context)
    

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
    return render(request,'admin_panel/product.html')

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
        
        return redirect('category')  

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
        return redirect('category')
    return redirect('category')




def sub(request):
    return render(request,'admin_panel/sub.html')

def create_subcategory(category_instance, subcategory_name):
    # Create and save a new Subcategory instance
    subcategory = Subcategory.objects.create(category=category_instance, name=subcategory_name)
    return subcategory

def add_sub(request):
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

def add_product(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product')  # Assuming you have a view for listing products
    else:
        form = ProductForm()

    return render(request, 'admin_panel/add_product.html', {
        'form': form,
        'categories': categories,
        'subcategories': subcategories,
    })