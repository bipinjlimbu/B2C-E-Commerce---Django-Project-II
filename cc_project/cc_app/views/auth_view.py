from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username:
            errors['username'] = 'Username is required.'
        if not password:
            errors['password'] = 'Password is required.'

        if errors:
            return render(request, 'auth/login_page.html', {'errors': errors, 'data': request.POST})
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'auth/login_page.html', {'errors': errors, 'data': request.POST})
        
    return render(request, 'auth/login_page.html')