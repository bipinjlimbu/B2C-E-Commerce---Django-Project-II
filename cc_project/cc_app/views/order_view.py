from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Order, OrderItem, CartItem

@login_required
def dispatch_order_view(request, order_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to dispatch orders.")
        return redirect('/')
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('/dashboard/admin/?section=order-fulfillment')

    if order.status != Order.Status.CONFIRMED:
        messages.error(request, "Only confirmed orders can be dispatched.")
        return redirect('/dashboard/admin/?section=order-fulfillment')

    order.status = Order.Status.SHIPPING
    order.save()
    messages.success(request, "Order dispatched successfully.")
    return redirect('/dashboard/admin/?section=order-fulfillment')

@login_required
def deliver_order_view(request, order_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to mark orders as delivered.")
        return redirect('/')
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('/dashboard/admin/?section=order-fulfillment')

    if order.status != Order.Status.SHIPPING:
        messages.error(request, "Only orders in transit can be marked as delivered.")
        return redirect('/dashboard/admin/?section=order-fulfillment')

    order.status = Order.Status.DELIVERED
    order.save()
    messages.success(request, "Order marked as delivered successfully.")
    return redirect('/dashboard/admin/?section=order-fulfillment')