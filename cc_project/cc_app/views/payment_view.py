from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import CartItem, Order, OrderItem
import requests
import json
import hmac
import hashlib
import base64
import uuid

def initiate_esewa_payment(request):
    if request.method == "POST":
        total_amount = request.POST.get('total_amount')
        payment_method = request.POST.get('payment_method')
        shipping_address = request.POST.get('shipping_address')
                    
        if payment_method != 'esewa':
            order = Order.objects.create(
                customer=request.user,
                total_amount=total_amount,
                transaction_id=str(uuid.uuid4()),
                status=Order.Status.PAID,
                shipping_address=shipping_address,
                payment_method=Order.PaymentMethod.COD
            )
            order.save()
            
            cart_items = CartItem.objects.filter(cart__customer=request.user)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price_at_purchase=item.product.price,
                    quantity=item.quantity
                )
                
                item.product.stock -= item.quantity
                item.product.save()
            
            cart_items.delete()
            messages.success(request, "Order placed successfully with Cash on Delivery.")
            return redirect('/dashboard/?section=pending-orders')
                
        
        # eSewa v2 is extremely strict: '100.0' and '100' create different hashes.
        # We ensure it matches the exact string that will be in the HTML form.
        try:
            total_val = float(total_amount)
            if total_val.is_integer():
                total_amount = str(int(total_val))
            else:
                total_amount = "{:.2f}".format(total_val) # Standardize decimal if exists
        except:
            return redirect('cart')

        transaction_uuid = str(uuid.uuid4())
        product_code = "EPAYTEST"
        
        # CORRECT SANDBOX SECRET KEY
        secret_key = "8gBm/:&EnhH.1/q" 
        
        # THE SIGNATURE FORMULA (No spaces after commas)
        # Sequence must be: total_amount,transaction_uuid,product_code
        data_to_sign = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
        
        # Generate HMAC-SHA256
        secret_key_bytes = secret_key.encode('utf-8')
        data_bytes = data_to_sign.encode('utf-8')
        hmac_sha256 = hmac.new(secret_key_bytes, data_bytes, hashlib.sha256).digest()
        
        # Base64 Encode
        signature = base64.b64encode(hmac_sha256).decode('utf-8')
        
        context = {
            'amount': total_amount,
            'shipping_address': shipping_address,
            'transaction_uuid': transaction_uuid,
            'product_code': product_code,
            'signature': signature,
            'esewa_url': "https://rc-epay.esewa.com.np/api/epay/main/v2/form",
            'success_url': "http://127.0.0.1:8000/payment/success/",
            'failure_url': "http://127.0.0.1:8000/payment/failed/",
        }
        
        return render(request, 'main/esewa_redirect_page.html', context)
    
    return redirect('cart')