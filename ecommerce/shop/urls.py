from django.urls import path
from . import views, admin_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_listing, name='product_listing'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),

    # Custom admin panel
    path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/add/', admin_views.admin_add_product, name='admin_add_product'),
    path('admin-panel/edit/<int:product_id>/', admin_views.admin_edit_product, name='admin_edit_product'),
    path('admin-panel/delete/<int:product_id>/', admin_views.admin_delete_product, name='admin_delete_product'),
    path('admin-panel/toggle/<int:product_id>/', admin_views.admin_toggle_stock, name='admin_toggle_stock'),
]