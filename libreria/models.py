from django.db import models
from django.forms import ValidationError

class Client(models.Model):
    first_name = models.CharField(max_length=75, null=False)
    last_name = models.CharField(max_length=75, null=False)
    dni = models.CharField(max_length=10, null=False)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=10, null=False)
    address = models.CharField(max_length=100, null=False)

    def clean(self):
        super().clean()
        if Client.objects.filter(dni=self.dni).exists():
            raise ValidationError({'dni': 'Cédula ya registrada'})
    
    def clean(self):
        super().clean()
        if Client.objects.filter(phone=self.phone).exists():
            raise ValidationError({'phone': 'Télefono ya registrado'})   

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
class Category(models.Model):
    category = models.CharField(max_length=30, null=False)

    def __str__(self) -> str:
        return self.category

class Product(models.Model):
    code = models.CharField(max_length=10, null=False, unique=True)
    book_title = models.CharField(max_length=200, null=False)
    year = models.IntegerField(null=False)
    author = models.CharField(max_length=75, null=False)
    publisher = models.CharField(max_length=75, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=1)
    condition = models.CharField(max_length=30, default='Nuevo')

    def __str__(self) -> str:
        return self.book_title
    
class Purchase(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    date = models.DateTimeField(auto_now_add=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.id} {self.client}'




