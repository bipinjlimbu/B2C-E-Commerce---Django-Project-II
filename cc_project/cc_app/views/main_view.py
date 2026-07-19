from django.shortcuts import render
from ..models import Product

def home_page(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:10]
    return render(request, 'main/home_page.html', {'products': products})