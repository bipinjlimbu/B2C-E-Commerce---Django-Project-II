from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Product, Order, Review
from django.db import models

@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access the admin dashboard.")
        return redirect('/')
    
    section = request.GET.get('section', 'customer-management')
    
    context = {
        'section': section,
        'awaiting_dispatch_count': Order.objects.filter(status='confirmed').count(),
        'awaiting_delivery_count': Order.objects.filter(status='shipping').count(),
        'delivered_count': Order.objects.filter(status='delivered').count(),
        'completed_count': Order.objects.filter(status='completed').count(),
        'cancelled_count': Order.objects.filter(status='cancelled').count(),
        'total_gross_revenue': Order.objects.filter(status='completed').aggregate(total=models.Sum('total_amount'))['total'] or 0,
    }
    
    if section == 'customer-management':
        context['customers'] = User.objects.filter(is_staff=False).order_by('-date_joined')
        
    elif section == 'product-management':
        context['products'] = Product.objects.all().order_by('-created_at')
        
    elif section == 'order-fulfillment':
        context['orders'] = Order.objects.all().order_by('-created_at')
        
    elif section == 'product-reviews':
        context['reviews'] = Review.objects.all().order_by('-created_at')
        
    elif section == 'revenue-logs':
        context['revenue_logs'] = Order.objects.filter(status='completed').order_by('-created_at')
        
    return render(request,'dashboard/admin_dashboard.html', context)

@login_required
def customer_dashboard_view(request):
    if request.user.is_staff:
        messages.error(request, "Staff members do not have a customer dashboard.")
        return redirect('/dashboard/admin/')
    
    section = request.GET.get('section', 'pending-orders')
    
    context = {
        'section': section,
        'gross_spent': Order.objects.filter(customer=request.user, status='completed').aggregate(total=models.Sum('total_amount'))['total'] or 0,
        'average_spent': Order.objects.filter(customer=request.user, status='completed').aggregate(average=models.Avg('total_amount'))['average'] or 0,
        
    }
    
    if section == 'pending-orders':
        context['pending_orders'] = Order.objects.exclude(customer=request.user, status__in=['completed', 'cancelled']).order_by('-created_at')
    elif section == 'my-orders':
        context['orders'] = Order.objects.filter(customer=request.user, status__in=['completed', 'cancelled']).order_by('-created_at')
    elif section == 'total-spent':
        context['total_spent'] = Order.objects.filter(customer=request.user, status='completed')
    elif section == 'my-reviews':
        context['my_reviews'] = Review.objects.filter(customer=request.user).order_by('-created_at')
        
    return render(request, 'dashboard/customer_dashboard.html', context)