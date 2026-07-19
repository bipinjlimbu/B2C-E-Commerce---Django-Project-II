from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access the admin dashboard.")
        return redirect('/')
    
    section = request.GET.get('section', 'customer-management')
    
    context = {
        'section': section,
    }
    
    if section == 'customer-management':
        context['customers'] = None
        
    elif section == 'product-management':
        context['products'] = None
        
    elif section == 'order-fulfillment':
        context['orders'] = None
        
    elif section == 'product-reviews':
        context['reviews'] = None
        
    elif section == 'revenue-logs':
        context['revenue_logs'] = None
        
    return render(request,'dashboard/admin_dashboard.html', context)