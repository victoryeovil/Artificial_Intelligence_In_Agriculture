from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.add_product, name='create_product'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('farmers/<int:pk>/', views.farmer_detail, name='farmer_detail'),
    path('farmers/create/', views.create_farmer, name='create_farmer'),
    path('farmers/<int:pk>/edit/', views.edit_farmer, name='edit_farmer'),
    path('farmers/<int:pk>/delete/', views.delete_farmer, name='delete_farmer'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
]
