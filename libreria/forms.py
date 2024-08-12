from django import forms 
from django.utils import timezone
from .models import Client, Category, Product, Purchase

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'first_name':forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control'}),
            'dni':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':forms.TextInput(attrs={'class': 'form-control'}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'category':forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'code':forms.TextInput(attrs={'class': 'form-control'}),
            'book_title':forms.TextInput(attrs={'class': 'form-control'}),
            'year':forms.TextInput(attrs={'class': 'form-control'}),
            'author':forms.TextInput(attrs={'class': 'form-control'}),
            'publisher':forms.TextInput(attrs={'class': 'form-control'}),
            'category':forms.Select(attrs={'class': 'form-control-file'}),
            'price':forms.NumberInput(attrs={'class': 'form-control'}),
            'stock':forms.NumberInput(attrs={'class': 'form-control'}),
            'condition':forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['client', 'product']
        widgets = {
            'client':forms.Select(attrs={'class': 'form-control-file'}),
            'product':forms.Select(attrs={'class': 'form-control-file'}),
        }
