from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100,null=False,unique=True)

    def _str_(self):
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length = 100,null= False,unique=True)
    
    def _str_(self):
        return self.brand_name

class Product(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    category = models.ForeignKey(Category,related_name='product', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,related_name='product', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image of {self.product.name}"
class Productsize(models.Model):
    product = models.ForeignKey(Product,related_name='productsize',on_delete=models.CASCADE)
    size = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.CharField(max_length = 255,blank = True)
    def __str__(self):
        return self.size
    
    

   