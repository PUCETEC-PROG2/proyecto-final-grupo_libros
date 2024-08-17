from django.db import models
from django.forms import ValidationError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    category = models.CharField(max_length=30, null=False)

    def __str__(self) -> str:
        return self.category
    
class Client(models.Model):
    first_name = models.CharField(max_length=75, null=False)
    last_name = models.CharField(max_length=75, null=False)
    dni = models.CharField(max_length=10, null=False, unique=True)
    email = models.EmailField(null=False, unique=True)
    phone = models.CharField(max_length=10, null=False)
    address = models.CharField(max_length=100, null=False)

    def clean(self):
        super().clean()

        try:
            validate_email(self.email)
        except ValidationError:
            raise ValidationError({'email': _('Ingrese un correo electrónico válido.')})

        if self.pk:
            if Client.objects.filter(dni=self.dni).exclude(pk=self.pk).exists():
                raise ValidationError({'dni': 'Cédula ya registrada'})
        else:
            if Client.objects.filter(dni=self.dni).exists():
                raise ValidationError({'dni': 'Cédula ya registrada'})

        if self.pk:
            if Client.objects.filter(email=self.email).exclude(pk=self.pk).exists():
                raise ValidationError({'email': 'Correo ya registrado'})
        else:
            if Client.objects.filter(email=self.email).exists():
                raise ValidationError({'email': 'Correo ya registrado'})
            
        if self.pk:
            if Client.objects.filter(phone=self.phone).exclude(pk=self.pk).exists():
                raise ValidationError({'phone': 'Teléfono ya registrado'})
        else:
            if Client.objects.filter(phone=self.phone).exists():
                raise ValidationError({'phone': 'Teléfono ya registrado'})

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
class Product(models.Model):
    code = models.CharField(max_length=10, null=False, unique=True)
    book_title = models.CharField(max_length=200, null=False)
    year = models.CharField(null=False)
    author = models.CharField(max_length=75, null=False)
    publisher = models.CharField(max_length=75, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    PRODUCT_CONDITION = {
        ('Nuevo', 'Nuevo'),
        ('Usado', 'Usado'),
        ('Mal estado', 'Mal estado'),
    }
    condition = models.CharField(max_length=30, choices=PRODUCT_CONDITION, null=False)
    picture = models.ImageField(upload_to='product_images')

    def __str__(self) -> str:
        return self.book_title
    
class Purchase(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False)

    def __str__(self) -> str:
        return f'{self.date} - Venta {self.id} - {self.client}'
    
class Purchase_Detail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount_product = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return f"{self.amount_product} x {self.product} en Venta {self.purchase.id}"
    





