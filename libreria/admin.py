from django.contrib import admin
from .models import Client, Category, Product, Purchase, Purchase_Detail

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    pass
@admin.register(Purchase_Detail)
class Pucharse_DetailAdmin(admin.ModelAdmin):
    pass