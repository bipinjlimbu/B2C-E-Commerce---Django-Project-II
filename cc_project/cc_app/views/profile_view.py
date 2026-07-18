from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User

@login_required
def profile_view(request):
    return render(request, 'main/profile_page.html')

@login_required
def edit_profile_view(request):
    return render(request, 'main/edit_profile_page.html')

@login_required
def delete_profile_view(request, user_id):
    if request.user.id != user_id and not request.user.is_staff:
        messages.error(request, 'You are not authorized to delete this profile.')
        return redirect('/')
    
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, 'Profile deleted successfully.')
    
    if request.user.is_staff:
        return redirect('/dashboard/admin/?section=customer-management')
    else:
        return redirect('/logout/')