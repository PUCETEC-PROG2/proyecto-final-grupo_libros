from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from .models import Client, Category, Product, Purchase, Purchase_Detail
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from libreria.forms import ClientForm, CategoryForm, ProductForm, PurchaseForm, DetailPurchaseFormSet

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
            return redirect('libreria:index')
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
            return redirect('libreria:index')
    else:
        form = ClientForm(instance=client)
        
    return render(request, 'client_form.html', {'form': form})

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, pk = client_id)
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
    purchase = get_object_or_404(Purchase_Detail, pk = purchase_id)
    template = loader.get_template('display_purchase.html')
    context = {
        'purchase': purchase
    }
    return HttpResponse(template.render(context, request))

@login_required
def list_purchase(request):
    purchases = Purchase_Detail.objects.order_by('purchase')
    template = loader.get_template('list_purchase.html')
    return HttpResponse(template.render({'purchases': purchases}, request))

@login_required
def add_purchase(request):
    if request.method == 'POST':
        purchase_form = PurchaseForm(request.POST)
        formset = DetailPurchaseFormSet(request.POST)

        if purchase_form.is_valid() and formset.is_valid():
            purchase = purchase_form.save()

            for form in formset:
                if form.cleaned_data:
                    product = form.cleaned_data.get('product')
                    amount_product = form.cleaned_data.get('amount_product')
                    
                    Purchase_Detail.objects.create(
                        purchase=purchase,
                        product=product,
                        amount_product=amount_product,
                        unit_price_product=product.price
                    )
            
            purchase.update_total()
            
            return redirect('libreria:list_purchase') 
    else:
        purchase_form = PurchaseForm()
        formset = DetailPurchaseFormSet()

    return render(request, 'purchase_form.html', {'purchase_form': purchase_form, 'formset': formset})