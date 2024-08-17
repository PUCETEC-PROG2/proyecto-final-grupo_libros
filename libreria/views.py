from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from .models import Client, Category, Product, Purchase, Purchase_Detail
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from libreria.forms import ClientForm, CategoryForm, ProductForm, PurchaseForm, PurchaseDetailForm
from django.contrib import messages
from django.utils import timezone
import pytz
class CustomLoginView(LoginView):
    template_name = 'login.html'

def index(request):
    template = loader.get_template('index.html')
    context = {
        'user': request.user,
        'logged_in': request.user.is_authenticated
    }
    return render(request, 'index.html', context)

# Category

def list_category(request):
    categorys = Category.objects.order_by('category')
    template = loader.get_template('list_category.html')
    context = {
        'categorys': categorys
    }
    return HttpResponse(template.render(context, request))

@login_required
def add_category(request):
    if request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('libreria:list_category')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form':form})

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk = category_id) 
    if request.method =='POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('libreria:list_category')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form':form})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk = category_id)
    category.delete()
    return redirect("libreria:list_category")

# Client

def client(request, client_id):
    client = get_object_or_404(Client, pk = client_id)
    template = loader.get_template('display_client.html')
    context = {
        'client': client
    }
    return HttpResponse(template.render(context, request))

@login_required
def list_client(request):
    clients = Client.objects.order_by('first_name')
    template = loader.get_template('list_client.html')
    return HttpResponse(template.render({'clients': clients}, request))

@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('libreria:list_client')
    else:
        form = ClientForm()
    
    return render(request, 'client_form.html', {'form': form})

@login_required
def edit_client(request, id):
    client = get_object_or_404(Client, pk = id)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('libreria:list_client')
    else:
        form = ClientForm(instance=client)
        
    return render(request, 'client_form.html', {'form': form})

@login_required
def delete_client(request, id):
    client = get_object_or_404(Client, pk = id)
    client.delete()
    return redirect("libreria:list_client")    

# Product

def product(request, product_id):
    product = get_object_or_404(Product, pk = product_id)
    template = loader.get_template('display_product.html')
    context = {
        'product': product
    }
    return HttpResponse(template.render(context, request))

def list_product(request):
    products = Product.objects.order_by('book_title')
    template = loader.get_template('list_product.html')
    return HttpResponse(template.render({'products': products}, request))

@login_required
def add_product(request):
    if request.method =='POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('libreria:list_product')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form':form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk = product_id) 
    if request.method =='POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('libreria:list_product')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form':form})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk = product_id)
    product.delete()
    return redirect("libreria:list_product")

# Purchase

def purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk = purchase_id)
    purchase_details = Purchase_Detail.objects.filter(purchase=purchase)
    context = {
        'purchase': purchase,
        'purchase_details': purchase_details,
    }
    return render(request, 'display_purchase.html', context)

@login_required
def list_purchase(request):
    purchases = Purchase.objects.order_by('date')
    template = loader.get_template('list_purchase.html')
    return HttpResponse(template.render({'purchases': purchases}, request))

@login_required
def add_purchase(request):
    clients = Client.objects.all()
    products = Product.objects.all()

    tz_local = pytz.timezone('America/Bogota')
    date_time = timezone.now().astimezone(tz_local).strftime('%Y-%m-%dT%H:%M')

    if request.method == 'POST':
        client_id = request.POST.get('client')
        date = request.POST.get('date')
        product_ids = request.POST.getlist('products[]')  
        amount_product = request.POST.getlist('amount_product[]') 

        # Validaciones
        if not client_id:
            messages.error(request, 'El ID del cliente no puede estar vacío.')
            return redirect('libreria:add_purchase')

        if not product_ids:
            messages.error(request, 'Debe seleccionar al menos un producto.')
            return redirect('libreria:add_purchase')

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            messages.error(request, 'Cliente no encontrado.')
            return redirect('libreria:add_purchase')

        total_price = 0
        purchase_details = []

        for units, product_id in enumerate(product_ids):
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                messages.error(request, 'Producto no encontrado.')
                return redirect('libreria:add_purchase')

            amount = int(amount_product[units])
            if amount <= 0:
                messages.error(request, f'La cantidad para el libro {product.book_title} no puede ser menor o igual a 0.')
                return redirect('libreria:add_purchase')

            if product.stock < amount:
                messages.error(request, f'No hay suficiente stock del libro: {product.book_title}.')
                return redirect('libreria:add_purchase')

            total = product.price * amount
            total_price += total

            purchase_details.append({
                'product': product,
                'amount': amount
            })

        if total_price <= 0:
            messages.error(request, 'El total de la venta debe ser mayor a 0.')
            return redirect('libreria:add_purchase')

        purchase = Purchase.objects.create(
            client=client,
            date=date,
            total_price=total_price, 
        )

        for detail in purchase_details:
            Purchase_Detail.objects.create(
                purchase=purchase,
                product=detail['product'],
                amount_product=detail['amount']
            )

            detail['product'].stock -= detail['amount']
            if detail['product'].stock < 0:
                detail['product'].stock = 0
            detail['product'].save()

        return redirect('libreria:list_purchase')

    context = {
        'clients': clients,
        'products': products,
        'date_time': date_time,
    }
    return render(request, 'purchase_form.html', context)