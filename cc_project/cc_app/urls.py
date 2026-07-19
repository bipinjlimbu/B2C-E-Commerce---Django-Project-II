from django.urls import path
from .views.auth_view import register_view, login_view, logout_view
from .views.main_view import home_page
from .views.profile_view import profile_view, edit_profile_view, delete_profile_view
from .views.products_view import products_view, add_product_view, edit_product_view, toggle_product_status_view, delete_product_view, single_product_view
from .views.cart_view import cart_view, add_to_cart_view, increase_cart_item_quantity_view, decrease_cart_item_quantity_view, remove_from_cart_view
from .views.payment_view import initiate_esewa_payment, payment_success_view
from .views.dashboard import admin_dashboard_view

urlpatterns = [
    path('', home_page, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/delete/<int:user_id>/', delete_profile_view, name='delete_profile'),
    path('products/', products_view, name='products'),
    path('products/add/', add_product_view, name='add_product'),
    path('products/edit/<int:product_id>/', edit_product_view, name='edit_product'),
    path('products/toggle-status/<int:product_id>/', toggle_product_status_view, name='toggle_product_status'),
    path('products/delete/<int:product_id>/', delete_product_view, name='delete_product'),
    path('products/<int:product_id>/', single_product_view, name='single_product'),
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/increase/<int:product_id>/', increase_cart_item_quantity_view, name='increase_cart_item_quantity'),
    path('cart/decrease/<int:product_id>/', decrease_cart_item_quantity_view, name='decrease_cart_item_quantity'),
    path('cart/remove/<int:product_id>/', remove_from_cart_view, name='remove_from_cart'),
    path('payment/initiate/', initiate_esewa_payment, name='initiate_payment'),
    path('payment/success/', payment_success_view, name='payment_success'),
    path('dashboard/admin/', admin_dashboard_view, name='admin_dashboard'),
]