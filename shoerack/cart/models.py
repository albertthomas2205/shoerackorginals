from django.db import models

# Create your models here.
from django.db import models
from user.models import CustomUser
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
        return f"Cart for "
   
    def get_total_amount(self):
        total_amount = 0
        for item in self.items.all():  # Accessing related CartItem objects using 'items' related_name
            total_amount += item.get_subtotal()
        return total_amount

  #  {self.user.name}


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Productsize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

       
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def get_subtotal(self):
        return self.product.price * self.quantity



class Usercoupon(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    
    
class Wishlist(models.Model):
    userr = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Productsize, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.userr)
    

    
