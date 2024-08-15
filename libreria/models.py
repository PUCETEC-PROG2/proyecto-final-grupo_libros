from django.db import models
from django.forms import ValidationError

class Category(models.Model):
    category = models.CharField(max_length=30, null=False)

    def __str__(self) -> str:
        return self.category
class Client(models.Model):
    first_name = models.CharField(max_length=75, null=False)
    last_name = models.CharField(max_length=75, null=False)
    dni = models.IntegerField(null=False)
    email = models.EmailField(null=False)
    phone = models.IntegerField(null=False)
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
    
class Product(models.Model):
    code = models.CharField(max_length=10, null=False, unique=True)
    book_title = models.CharField(max_length=200, null=False)
    year = models.IntegerField(null=False)
    author = models.CharField(max_length=75, null=False)
    publisher = models.CharField(max_length=75, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=1)
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
    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f'Venta {self.id} - {self.client}'
    
    def update_total_price(self):
        self.total_price = sum(purchase.subtotal() for purchase in self.purchase.all())
        self.save()

class Purchase_Detail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount_product = models.PositiveIntegerField()
    unit_price_product = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.amount_product * self.unit_price_product
    
    def __str__(self) -> str:
        return f"{self.amount_product} x {self.product} en Venta {self.purchase.id}"
    



