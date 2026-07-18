from django.urls import path
from .views.auth_view import login_view, logout_view
from .views.main_view import home_page

urlpatterns = [
    path('', home_page, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]