from django import forms 
from .models import Client, Category, Product, Purchase, Purchase_Detail
from django.forms import formset_factory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'category':forms.TextInput(attrs={'class': 'form-control'}),
        }
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'first_name':forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control'}),
            'dni':forms.NumberInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':forms.NumberInput(attrs={'class': 'form-control'}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni and not str(dni).isdigit():
            raise forms.ValidationError('El DNI debe contener solo números.')
        return dni
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not str(phone).isdigit():
            raise forms.ValidationError('El número de teléfono debe contener solo números y empezar por "09".')
        return phone

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
            'condition':forms.Select(attrs={'class': 'form-control-file'}),
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['client']
        widgets = {
            'client':forms.Select(attrs={'class': 'form-control-file'}),
        }

class PurchaseDetailForm(forms.ModelForm):
    class Meta:
        model = Purchase_Detail
        fields = ['product', 'amount_product']
        widgets = {
            'product':forms.Select(attrs={'class': 'form-control-file'}),
            'amount_product':forms.NumberInput(attrs={'class': 'form-control'}),
        }


DetailPurchaseFormSet = formset_factory(PurchaseDetailForm, extra=1)