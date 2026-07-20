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

@login_required
def complete_order_view(request, order_id):
    if request.user.is_staff:
        messages.error(request, "You do not have permission to complete orders.")
        return redirect('/')
    
    try:
        order = Order.objects.get(id=order_id, customer=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('/dashboard/?section=pending-orders')

    if order.status != Order.Status.DELIVERED:
        messages.error(request, "Only delivered orders can be marked as completed.")
        return redirect('/dashboard/?section=pending-orders')

    order.status = Order.Status.COMPLETED
    order.save()
    messages.success(request, "Order marked as completed successfully.")
    return redirect('/dashboard/?section=pending-orders')

@login_required
def cancel_order_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id, customer=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('/dashboard/?section=pending-orders')

    if order.status in [Order.Status.CONFIRMED, Order.Status.SHIPPING, Order.Status.DELIVERED]:
        order.status = Order.Status.CANCELLED
        order.save()
        messages.success(request, "Order cancelled successfully.")
    else:
        messages.error(request, "Only confirmed or in-transit orders can be cancelled.")

    return redirect('/dashboard/?section=pending-orders')