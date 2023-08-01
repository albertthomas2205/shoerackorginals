
from django import forms
from .models import Product,ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'stock', 'color', 'size', 'price', 'category', 'subcategory']


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ProductImage
        fields = ('image',)