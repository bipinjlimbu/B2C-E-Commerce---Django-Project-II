from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Product, Cart, CartItem

@login_required
def add_to_cart_view(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.user.is_staff:
        messages.error(request, "Staff members cannot add products to the cart.")
        return redirect('/products/')
    
    if not product.is_active:
        messages.error(request, "This product is currently unavailable.")
        return redirect('/products/')
    
    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect('/products/')
    
    if CartItem.objects.filter(product=product, cart__customer=request.user).exists():
        messages.info(request, f"{product.name} is already in your cart. Quantity updated.")
        return redirect('/products/')
    
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
        
    messages.success(request, f'Added {product.name} to your cart.')
    return redirect('/products/')

@login_required
def cart_view(request):
    if request.user.is_staff:
        messages.error(request, "Staff members do not have a shopping cart.")
        return redirect('/products/')
    
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_items = CartItem.objects.filter(cart=cart)    
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'main/cart_page.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart_view(request, product_id):
    if request.user.is_staff:
        messages.error(request, "Staff members do not have a shopping cart.")
        return redirect('/products/')
    
    try:
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(customer=request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        messages.success(request, f'Removed {product.name} from your cart.')
    except CartItem.DoesNotExist:
        messages.error(request, "Cart item not found.")
    
    return redirect('/cart/')