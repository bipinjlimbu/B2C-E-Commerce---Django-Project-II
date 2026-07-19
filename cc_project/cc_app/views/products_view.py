from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Product

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