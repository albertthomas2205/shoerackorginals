from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100,null=False,unique=True)

    def _str_(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)

    def _str_(self):
        return self.name

# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     stock = models.IntegerField()
#     color = models.CharField(max_length=255)
#     size = models.IntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='product_images/')

#     def __str__(self):
#         return self.name



class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    stock = models.IntegerField()
    color = models.CharField(max_length=255)
    size = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image of {self.product.name}"

    