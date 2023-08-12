from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from cart.models import Cart, CartItem
from adminside.models import Product,Productsize
# from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_POST
from user.models import Userdetails,CustomUser
from .models import Cart, CartItem
from django.http import JsonResponse

def add_to_cart(request, product_id):
    # Get the product using the product_id from the request
    product = Productsize.objects.get(pk=product_id)

    # Get the user's cart or create a new cart if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Add the product to the cart or update its quantity if it already exists
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
 

    return redirect('product_detail',product_id)  # Redirect to the cart page after adding the item




from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Productsize, Cart, CartItem,Order,OrderItem




def show_cart(request):
    user = request.user  # Assuming you have implemented authentication and you are using the request.user to get the current user
    user_cart = Cart.objects.get(user=user)
    total_amount = user_cart.get_total_amount()

    context = {
        'cart': user_cart,
        'total_amount': total_amount,
    }

    return render(request, 'cartside/cart.html', context)



from decimal import Decimal

def checkout(request):
    addresses = Userdetails.objects.filter(userr=request.user)
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Calculate the total price of items in the cart
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    # Convert the Decimal total_price to a float
    total_price_float = float(total_price)
    
    # Add shipping charges and estimate tax
    shipping_charges = 150
    tax_percentage = 0.05
    estimated_tax = total_price_float * tax_percentage
    
    # Calculate the final total price including shipping and tax
    final_total = total_price_float + shipping_charges + estimated_tax
    
    context = {
        'addresses': addresses,
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_charges': shipping_charges,
        'estimated_tax': estimated_tax,
        'final_total': final_total,
    }
    return render(request, 'cartside/checkout.html', context)





def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.cart.user == request.user:
        cart_item.delete()

    return redirect('cart') 

from django.http import HttpResponseForbidden




def car(request):
   
    return render(request, 'cartside/cart.html')

from django.shortcuts import render
from .models import Userdetails

from django.shortcuts import render
from .models import Cart

from django.http import JsonResponse
def tril (request):
   
    product = Product.objects.get(id=2)
    context = {'product':product}
    return render(request,'cartside/tril.html',context)

        
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'cartside/tril.html', {'product': product})

from django.http import JsonResponse
from .models import Product, Productsize

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
        
def order(request):
    
    return render(request,'cartside/orders.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cart, CartItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from cart.models import CartItem  # Import the CartItem model




from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import CartItem

@require_POST
def update_cart_quantity(request):
    if request.method == 'POST':
        print("haiiii")
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        print(quantity)
        # Get the cart item and update the quantity
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
        
        # You can also recalculate the cart total here if needed
        
        return JsonResponse({'success': True, 'message': 'Quantity updated successfully.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def create_order(request):
    if request.method=='POST':
        add=request.POST.get('address')
        payment=request.POST.get('pay-method')
        cart = get_object_or_404(Cart, user=request.user)
        address=get_object_or_404(Userdetails,id=add )
        total_amount = Decimal(0)
        for cart_item in cart.items.all():
            total_amount += cart_item.product.price * cart_item.quantity
        total_amount = total_amount.quantize(Decimal('0.01'))
        order = Order.objects.create(user=request.user,address=address,total_amount=total_amount)
        for cart_item in cart.items.all():
            OrderItem.objects.create(order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            payment=payment,
            total_itemprice=cart_item.product.price * cart_item.quantity )
        for cart_item in cart.items.all():
            product = cart_item.product
            product.stock -= cart_item.quantity
            product.save()
        cart.items.all().delete()    
        return render(request,'cartside/thankyou.html')
    return render(request,'cartside/thankyou.html')

def userorders(request):
    cust = get_object_or_404(CustomUser, id=request.user.id)
    orders=Order.objects.filter(user=cust)
    
    context={'orders':orders,'cust':cust}
    return render(request,'cartside/orders.html',context)

def Usercancel(request,id):
    edit=get_object_or_404(Order,id=id)
    edit.status='C'
    edit.save()
    return redirect('userorders')
