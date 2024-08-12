from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from .models import Client, Category, Product, Purchase
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from libreria.forms import ClientForm, CategoryForm, ProductForm, PurchaseForm



