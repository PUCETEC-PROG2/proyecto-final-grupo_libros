from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from .models import Client, Category, Product, Purchase
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from libreria.forms import ClientForm, CategoryForm, ProductForm, PurchaseForm
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from .models import Client, Category
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from libreria.forms import ClientForm, CategoryForm


def client(request, client_id):
    client = get_object_or_404(Client, pk = client_id)
    template = loader.get_template('display_clientes.html')
    context = {
        'client': client
    }
    return HttpResponse(template.render(context, request))

def categorys(request, categorys_id):
    client = get_object_or_404(Category, pk = categorys_id)
    template = loader.get_template('display_categorias.html')
    context = {
        'categorys': categorys
    }
    return HttpResponse(template.render(context, request))


    
    
    
    

