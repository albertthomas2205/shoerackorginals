from django.db import models

# Create your models here.
from django.db import models
from user.models import CustomUser
from account.models import Userdetails,Coupon
from adminside.models import Product,ProductImage,Productsize
from django.template.defaultfilters import slugify



# class Cart(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     coupon = models.ForeignKey(Coupon,on_delete=models.DO_NOTHING,null=True,blank=True )
#     def __str__(self):
#         return f"Cart for {self.user.name}"
#     def get_total_amount(self):
#         total_amount = 0
#         for item in self.items.all():  # Accessing related CartItem objects using 'items' related_name
#             total_amount += item.get_subtotal()
#         return total_amount

 




    
class Wishlist(models.Model):
    userr = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Productsize, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.userr)
    

    

    
