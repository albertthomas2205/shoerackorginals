from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from cart.models import Cart, CartItem
from adminside.models import Product,Productsize
# from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_POST
from user.models import Userdetails,CustomUser
from .models import Cart, CartItem,Wishlist,Coupon,Usercoupon
from django.http import JsonResponse
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Productsize, Cart, CartItem,Order,OrderItem
from django.db.models import F, Q, Sum


@login_required(login_url='loginn') 
def add_to_cart(request,id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Productsize, id=id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    bag=CartItem.objects.all()
    request.session['item_added_to_cart'] = True
    id = product.product_id
    print(id)
   
    return redirect('product_detail',id)
      






@login_required(login_url='loginn')  # Redirect to 'loginn' if not logged in
def show_cart(request):
    user = request.user
    user_cart = Cart.objects.get(user=request.user)
    total_amount = user_cart.get_total_amount()
    cartitems = CartItem.objects.filter(cart=user_cart)
  
    for cart in cartitems:
        print(cart.product.product.name) 
    

    context = {
        'cart': user_cart,
        'total_amount': total_amount,
        'cartitems':cartitems
    }
    

    return render(request, 'cartside/cart.html', context)

@login_required(login_url='loginn')
def CartDetail(request):
    cart, create = Cart.objects.get_or_create(user=request.user)
    cartitems = CartItem.objects.filter(cart=cart)
    numitems = cartitems.count()
    cartitems = cartitems.annotate(
        total_product_price=F("product__price") * F("quantity")
    )
    total_price = cartitems.aggregate(Sum("total_product_price"))[
        "total_product_price__sum"
    ]
    subtotal = total_price
    coupon_discount = Decimal(0)  # Initialize coupon discount

    if cart.coupon is not None:
        coup = get_object_or_404(Coupon, id=cart.coupon.id)
        coupon_discount = Decimal(coup.discount)
        total_price -= coupon_discount

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.valid_from <= timezone.now() <= coupon.valid_to:
                    cart.coupon = coupon
                    cart.save()
                    return redirect('cart_detail')
            except Coupon.DoesNotExist:
                pass

    total_stock = sum(item.product.stock for item in cartitems)
    context = {
        "cart_items": cartitems,
        "total_price": total_price,
        "total_stock": total_stock,
        "numitems": numitems,
        "cart": cart,
        "subtotal": subtotal,
        "coupon_discount": coupon_discount,  # Pass the coupon discount to the template
    }
    return render(request, "cartside/cart.html", context)

from decimal import Decimal

def Removecoupon(request):
    cart = get_object_or_404(Cart, user=request.user)
    usercoupon = Usercoupon.objects.get(Q(coupon=cart.coupon) & Q(user=request.user))
    usercoupon.delete()
    cart.coupon = None
    cart.save()
    return redirect("cartdetail")

def apply_coupon(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_items = cart_items.annotate(
        total_product_price=F("product__price") * F("quantity")
    )
    total_price = cart_items.aggregate(Sum("total_product_price"))[
        "total_product_price__sum"
    ]
    if request.method == "POST":
        code = request.POST.get("code")
        try:
            coup = Coupon.objects.get(code=code)
            k = coup.minimumamount
            if Usercoupon.objects.filter(Q(coupon=coup) & Q(user=request.user)).exists():
                key = "2"
                messages.error(request, f"coupon alredy . ({key})")
                return redirect("cart")
                
                
                
            elif k > total_price:
                
                key = "2"
                messages.error(request, f"invalid otp. ({key})")
                return redirect("cart")
                    
            elif coup.active == False:
                key = "2"
                messages.error(request, f"invalid otp. ({key})")
                return redirect("cart")
                
            else:
                cart.coupon = coup
                cart.save()
                user = get_object_or_404(CustomUser, id=request.user.id)
                Usercoupon.objects.create(user=user, coupon=coup)
                x = coup.discount
                discount = Decimal(x)
                total_price -= discount
                key = "2"
                messages.error(request, f"invalid otp. ({key})")
                return redirect("cart")
        except:
                key = "2"
                messages.error(request, f"invalid coupon name. ({key})")
                return redirect("cart")
                
        
            
  



def thanku(request):
    return render(request, "thanku.html")



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


from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem, Coupon, Order, OrderItem

from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem, Coupon, Order, OrderItem

def create_order(request):
    if request.method == 'POST':
        address_id = request.POST.get('address')
        payment = request.POST.get('pay-method')
        
        # Get the user's cart
        cart = get_object_or_404(Cart, user=request.user)
        
        # Get the selected address
        address = get_object_or_404(Userdetails, id=address_id)
        
        # Calculate total price of items in the cart
        total_price = cart.get_total_amount()
        
        # Check if a coupon is applied
        coupon_discount = 0
        if cart.coupon:
            coupon = get_object_or_404(Coupon, id=cart.coupon.id)
            coupon_discount = Decimal(coupon.discount)
            total_price -= coupon_discount
        
        # Create the order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=total_price,  # Adjust this field based on your model
            coupon_applied=cart.coupon if cart.coupon else None,
        )
        
        # Create order items and update product stock
        for cart_item in cart.items.all():
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                total_itemprice=cart_item.get_subtotal() - coupon_discount,
            )
            # Update product stock
            product = cart_item.product
            product.stock -= cart_item.quantity
            product.save()

        # Clear the cart after successful order
        cart.items.all().delete()

        return render(request, 'cartside/thankyou.html')

    return render(request, 'cartside/thankyou.html')




def userorders(request):
    cust = get_object_or_404(CustomUser, id=request.user.id)
    orders = Order.objects.filter(user=cust).order_by('-created_at')

    # Debugging statements
    for order in orders:
        print(order.created_at)

    context = {'orders': orders, 'cust': cust}
    return render(request, 'cartside/orders.html', context)

def Usercancel(request,id):
    edit=get_object_or_404(Order,id=id)
    edit.status='C'
    edit.save()
    return redirect('userorders')

def wishlist(request):
    user = request.user
    wproducts = Wishlist.objects.filter(userr=user)
    context = {"wproducts": wproducts}
    return render(request, "cartside/wishlist.html", context)


def Addwishlist(request, id):
    user = request.user
    product = Productsize.objects.get(id=id)
    Wishlist.objects.create(userr=user, product=product)
    return redirect("singproduct", id)


def Deletewishlist(request, id):
    d = Wishlist.objects.get(id=id)
    d.delete()
    return redirect("wishlist")








