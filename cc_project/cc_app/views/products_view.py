from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from ..models import User, Product

@login_required
def products_view(request):
    products = Product.objects.all().order_by('-created_at')
    category = request.GET.get('category')
    availability = request.GET.get('availability')
    price_range = request.GET.get('price_range')
    sort = request.GET.get('sort')
    q = request.GET.get('q')
    
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(category__icontains=q))
        
    if category:
        products = products.filter(category=category)
        
    if availability == 'available':
        products = products.filter(stock__gt=0, is_active=True)
    elif availability == 'masterworks':
        products = products.filter(stock=1, is_active=True)
        
    if price_range:
        if price_range == '0-999':
            products = products.filter(price__lt=1000)
        elif price_range == '1000-4999':
            products = products.filter(price__gte=1000, price__lt=5000)
        elif price_range == '5000-9999':
            products = products.filter(price__gte=5000, price__lt=10000)
        elif price_range == '10000-49999':
            products = products.filter(price__gte=10000, price__lt=50000)
        elif price_range == '50000+':
            products = products.filter(price__gte=50000)
            
    if sort:
        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'newest':
            products = products.order_by('-created_at')
        elif sort == 'oldest':
            products = products.order_by('created_at')
        
    return render(request, 'main/products_page.html', {'products': products})

@login_required
def add_product_view(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to add products.")
        return redirect('/')
    
    errors = {}
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '').strip()
        stock = request.POST.get('stock', '').strip()
        is_active = request.POST.get('is_active') == 'true'
        product_image = request.FILES.get('product_image')

        if not name:
            errors['name'] = "Product name is required."
        if not category:
            errors['category'] = "Category is required."
        if not description:
            errors['description'] = "Description is required."
        if not price:
            errors['price'] = "Price is required."
        if not stock:
            errors['stock'] = "Stock quantity is required."
        if not product_image:
            errors['product_image'] = "Product image is required."

        if errors:
            return render(request, 'main/add_products_page.html', {'errors': errors, 'data': request.POST})
        
        product = Product(
            name=name,
            category=category,
            description=description,
            price=price,
            stock=stock,
            is_active=is_active,
            product_image=product_image
        )
        product.save()
        messages.success(request, f"Product '{product.name}' added successfully.")
        return redirect('/dashboard/admin/?section=product-management')
    
    return render(request, 'main/add_products_page.html')

@login_required
def edit_product_view(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to edit products.")
        return redirect('/')
    
    if not product:
        messages.error(request, "Product not found.")
        return redirect('/dashboard/admin/?section=product-management')
    
    errors = {}
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '').strip()
        stock = request.POST.get('stock', '').strip()
        is_active = request.POST.get('is_active') == 'true'
        product_image = request.FILES.get('product_image')
        
        if not name:
            errors['name'] = "Product name is required."
        if not category:
            errors['category'] = "Category is required."
        if not description:
            errors['description'] = "Description is required."
        if not price:
            errors['price'] = "Price is required."
        if not stock:
            errors['stock'] = "Stock quantity is required."
        if errors:
            return render(request, 'main/edit_products_page.html', {'errors': errors, 'data': request.POST, 'product': product})
        
        product.name = name
        product.category = category
        product.description = description
        product.price = price
        product.stock = stock
        product.is_active = is_active
        if product_image:
            product.product_image = product_image
        product.save()
        messages.success(request, f"Product '{product.name}' updated successfully.")
        return redirect('/dashboard/admin/?section=product-management')
    
    return render(request, 'main/edit_products_page.html', {'product': product})

@login_required
def toggle_product_status_view(request, product_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to change product status.")
        return redirect('/')
    
    try:
        product = Product.objects.get(id=product_id)
        product.is_active = not product.is_active
        product.save()
        status = "activated" if product.is_active else "deactivated"
        messages.success(request, f"Product '{product.name}' has been {status}.")
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
    
    return redirect('/dashboard/admin/?section=product-management')

@login_required
def delete_product_view(request, product_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to delete products.")
        return redirect('/')
    
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted successfully.")
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
    
    return redirect('/dashboard/admin/?section=product-management')