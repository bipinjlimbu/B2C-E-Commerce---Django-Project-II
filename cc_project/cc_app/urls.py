from django.urls import path
from .views.auth_view import register_view, login_view, logout_view
from .views.main_view import home_page
from .views.profile_view import profile_view

urlpatterns = [
    path('', home_page, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
]