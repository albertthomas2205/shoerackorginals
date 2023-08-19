from django.db import models

# Create your models here.
from django.db import models
from user.models import CustomUser,Userdetails
from adminside.models import Product,ProductImage,Productsize
from django.template.defaultfilters import slugify

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    minimumamount = models.IntegerField()
    discount = models.FloatField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.code

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.DO_NOTHING,null=True,blank=True )
    def __str__(self):
        return f"Cart for {self.user.name}"
    def get_total_amount(self):
        total_amount = 0
        for item in self.items.all():  # Accessing related CartItem objects using 'items' related_name
            total_amount += item.get_subtotal()
        return total_amount

 


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Productsize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

       
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def get_subtotal(self):
        return self.product.price * self.quantity

# class Order(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     address = models.ForeignKey(Userdetails,on_delete=models.CASCADE)
#     total_amount = models.DecimalField( max_digits=10,decimal_places=2)
#     order_status_choices = [
#         ('P', 'Processing'),
#         ('S', 'Shipped'),
#         ('D', 'Delivered'),
#         ('C', 'Cancelled'),
#     ]
#     status = models.CharField(max_length=1, choices=order_status_choices, default='P')

#     def __str__(self):
#         return f"Order {self.pk} for {self.user.username}"



# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Productsize, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=0)
#     payment = models.CharField(max_length=20)
#     total_itemprice = models.DecimalField( max_digits=10,decimal_places=2)

#     def __str__(self):
#         return f"{self.product.name} - {self.quantity}"
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Userdetails,on_delete=models.DO_NOTHING)
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    razor_pay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_signature=models.CharField(max_length=100,null=True,blank=True)
    slug  = models.CharField(max_length=200,null=True,blank=True)
    payment_method = models.CharField(max_length=20)
    coupon_applied=models.ForeignKey(Coupon,on_delete=models.DO_NOTHING,null=True,blank=True)
    def __str__(self):
        return f"Order {self.pk} for {self.user.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.user.id) +str(self.created_at))
        return super().save(*args, **kwargs)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Productsize, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=0)
    order_status_choices = [
        ('P', 'Processing'),
        ('S', 'Shipped'),
        ('O', 'Out For Delivery'),
        ('D', 'Delivered'),
        ('C', 'Cancelled'),
    ]
    status = models.CharField(max_length=1, choices=order_status_choices, default='P')
    total_itemprice=models.DecimalField(max_digits=10, decimal_places=2)
    order_status_choices = [
        ('P', 'Pending'),
        ('S', 'Recieved'),
    ]
    payment_status = models.CharField(max_length=1, choices=order_status_choices, default='P')

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"




class Usercoupon(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    
    
class Wishlist(models.Model):
    userr = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Productsize, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.userr)
    
