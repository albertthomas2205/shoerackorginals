from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from account.models import Cart, CartItem,Coupon
from adminside.models import Product,Productsize,ProductImage
from cart.models import Usercoupon,Wishlist
from django.contrib.auth.decorators import login_required
from user.models import CustomUser
from account.models import Userdetails
from django.http import JsonResponse
from django.utils import timezone
from django.http import JsonResponse
from account.models import Order,OrderItem
from django.db.models import F, Q, Sum
from decimal import Decimal
from django.views.decorators.http import require_POST
from django.contrib import messages
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt




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

def get_product_size_id(request):
    selected_size = request.GET.get('size')
    try:
        product_size = Productsize.objects.get(size=selected_size)
        product_size_id = product_size.id
        return JsonResponse({'product_size_id': product_size_id})
    except Productsize.DoesNotExist:
        return JsonResponse({'error': 'Size not found'}, status=400)

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
    return render(request, "cartside/thankyou.html")



def checkout(request):
    address = Userdetails.objects.filter(userr=request.user).order_by("-created_at")
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    k = 15
    total_price = (
        int(sum((item.product.price * item.quantity for item in cart_items))) + k
    )

    subtotal = total_price
    dis = 0
    if cart.coupon is not None:
        coup = get_object_or_404(Coupon, id=cart.coupon.id)
        dis = coup.discount
        total_price -= dis
    numitems = cart_items.count()
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    payment = client.order.create(
        {"amount": total_price * 100, "currency": "INR", "payment_capture": 1}
    )
    print(payment)
    context = {
        "addresses": address,
        "cart_items": cart_items,
        "total_price": total_price,
        "numitems": numitems,
        "dis": dis,
        "subtotal": subtotal,
        "payment": payment,
    }
    return render(request, "cartside/checkout.html", context)





def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.cart.user == request.user:
        cart_item.delete()

    return redirect('cart') 

from django.http import HttpResponseForbidden





def tril (request):
   
    product = Product.objects.get(id=2)
    context = {'product':product}
    return render(request,'cartside/tril.html',context)

        
# def product_detail_view(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     return render(request, 'cartside/tril.html', {'product': product})

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




# def create_orders(request):
#     cart = get_object_or_404(Cart, user=request.user)
#     total_price = Decimal(0)
#     add = request.session.get("selected_address")
#     payment1 = request.session.get("pay-method")
#     address = get_object_or_404(Userdetails, id=add)
#     for cart_item in cart.items.all():
#         total_price += cart_item.product.price * cart_item.quantity
#     try:
#         coup = get_object_or_404(Coupon, id=cart.coupon.id)
#         dis = coup.discount
#         di = Decimal(dis)
#         total_price -= di
#         order = Order.objects.create(
#             user=request.user,
#             address=address,
#             total_price=total_price,
#             payment_method=payment1,
#             coupon_applied=coup,
#         )
#     except:
#         order = Order.objects.create(
#             user=request.user,
#             address=address,
#             total_price=total_price,
#             payment_method=payment1,
#         )
#     for cart_item in cart.items.all():
#         OrderItem.objects.create(
#             order=order,
#             product=cart_item.product,
#             quantity=cart_item.quantity,
#             total_itemprice=cart_item.product.price * cart_item.quantity,
#         )
#     for cart_item in cart.items.all():
#         product = cart_item.product
#         product.stock -= cart_item.quantity
#         product.save()
#     cart.items.all().delete()
#     cart.coupon = None
#     cart.save()
#     return render(request, "cartside/thankyou.html")




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

def selectaddress(request):
    if request.method == "POST":
        add = request.POST.get("address")
        paymen = request.POST.get("pay-method")
        print(paymen)
        request.session["selected_address"] = add
        request.session["pay-method"] = paymen
        if paymen != "Upi":
            return redirect("thankyou")
        return JsonResponse({"message": "Order placed successfully"})

    return JsonResponse({"message": "Invalid request method"})

def create_orders(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = Decimal(0)
    add = request.session.get("selected_address")
    payment1 = 'COD'
    address = get_object_or_404(Userdetails, id=add)
    for cart_item in cart.items.all():
        total_price += cart_item.product.price * cart_item.quantity
    try:
        coup = get_object_or_404(Coupon, id=cart.coupon.id)
        dis = coup.discount
        di = Decimal(dis)
        total_price -= di
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total_price,
            payment_method=payment1,
            coupon_applied=coup,
        )
    except:
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total_price,
            payment_method=payment1,
        )
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            total_itemprice=cart_item.product.price * cart_item.quantity,
        )
    for cart_item in cart.items.all():
        product = cart_item.product
        product.stock -= cart_item.quantity
        product.save()
    message = "Order placed successfully"
    cart.items.all().delete()
    cart.coupon = None
    cart.save()
    return render(request, "cartside/thankyou.html")

@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = Decimal(0)
    add = request.session.get("selected_address")
    payment1 = request.session.get("pay-method")
    address = get_object_or_404(Userdetails, id=add)
    for cart_item in cart.items.all():
        total_price += cart_item.product.price * cart_item.quantity
    try:
        coup = get_object_or_404(Coupon, id=cart.coupon.id)
        dis = coup.discount
        di = Decimal(dis)
        total_price -= di
        total_price_float = float(total_price)
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total_price,
            payment_method=payment1,
            coupon_applied=coup,
        )
    except:
        total_price_float = float(total_price)
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total_price,
            payment_method=payment1,
        )
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    payment = client.order.create(
        {
            "amount": int(total_price_float * 100),
            "currency": "INR",
            "payment_capture": 1,
        }
    )
    order.razor_pay_payment_id = payment["id"]
    order.save()
    print(payment["id"])
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            total_itemprice=cart_item.product.price * cart_item.quantity,
        )
    for cart_item in cart.items.all():
        product = cart_item.product
        product.stock -= cart_item.quantity
        product.save()
    message = "Order placed successfully"
    cart.items.all().delete()
    cart.coupon = None
    cart.save()
    return render(request, "cartside/thankyou.html")

# @csrf_exempt
# @require_POST
# def add_to_cart(request):
#     product_size_id = request.POST.get('product_size_id')
#     selected_size = request.POST.get('selected_size')  # Get the selected size
    
#     try:
#         product_size = Productsize.objects.get(id=product_size_id)

        
#         response_data = {'success': True, 'message': 'Product added to cart.'}
#     except Productsize.DoesNotExist:
#         response_data = {'success': False, 'message': 'Product size not found.'}
    
#     return JsonResponse(response_data)








