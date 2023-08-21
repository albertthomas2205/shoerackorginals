
from django import forms
from .models import Product,ProductImage,Productsize
from account.models import Userdetails

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'color', 'category','brand']


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ProductImage
        fields = ('image',)
        
class ProductsizeForm(forms.ModelForm):
    class Meta:
        model = Productsize
        fields = ['stock','description','price','size']
        
class UserdetailsForm(forms.ModelForm):
    class Meta:
        model = Userdetails
        fields = ['custom_name', 'house_name', 'landmark', 'pincode', 'city', 'state', 'alternative_ph']
       
      
      