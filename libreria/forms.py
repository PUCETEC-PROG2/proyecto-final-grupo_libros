from django import forms 
from .models import Client, Category, Product, Purchase, Purchase_Detail
from django.core.exceptions import ValidationError

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
            'dni':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':forms.TextInput(attrs={'class': 'form-control'}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'dni': 'Cédula',
            'email': 'Correo Electrónico',
            'phone': 'Número de teléfono',
            'address': 'Dirección',
        }
        error_messages = {
            'email':{
            'invalid': 'Ingrese una dirección de correo electrónico válida.',
            }
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        try:
            dni = int(dni)
        except (TypeError, ValueError):
            raise forms.ValidationError('El campo de cédula solo admite valores numéricos.')

        if dni < 0:
            raise forms.ValidationError('El campo de cédula no admite valores negativos.')
        return dni

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
        labels = {
            'code': 'Código del producto',
            'book_title': 'Título del Libro',
            'year': 'Año de Publicación',
            'author': 'Autor',
            'publisher': 'Editorial',
            'category': 'Género',
            'price': 'Precio',
            'stock': 'Stock',
            'condition': 'Condición',
        }

    def clean_year(self):
        year = self.cleaned_data.get('year')
        try:
            year = int(year)
        except (TypeError, ValueError):
            raise forms.ValidationError('Año inválido. Debe ser un número entero.')

        if year < 0:
            raise forms.ValidationError('El año no puede ser negativo.')
        return year
    
    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price < 0:
            raise ValidationError("El precio del libro no puede ser negativo.")

        return price
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')

        if stock < 0:
            raise ValidationError("El stock no puede ser negativo.")

        return stock

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['client', 'date']
        widgets = {
            'client':forms.Select(attrs={'class': 'form-control-file'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        labels = {
            'client': 'Cliente',
            'date': 'Fecha',
        }

class PurchaseDetailForm(forms.ModelForm):
    class Meta:
        model = Purchase_Detail
        fields = ['product', 'amount_product']
        widgets = {
            'product':forms.Select(attrs={'class': 'form-control-file'}),
            'amount_product':forms.NumberInput(attrs={'class': 'form-control', 'min':1}),
        }
        labels = {
            'product': 'Libro',
            'amount_product': 'Unidades del producto',
        }
        
    def clean(self):
            cleaned_data = super().clean()
            product = cleaned_data.get('product')
            amount_product = cleaned_data.get('amount_product')

            if product and amount_product:
                if amount_product > product.stock: 
                    self.add_error('amount_product', f'La cantidad supera al stock disponible de este producto. Unidades existentes: {product.stock}')
