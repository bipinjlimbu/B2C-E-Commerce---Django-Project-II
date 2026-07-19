from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Product

@login_required
def add_product_view(request):
    return render(request, 'main/add_products_page.html')