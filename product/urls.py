from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('new/', views.new_product, name='new'),
    path('<str:product_pk>/', views.product_detail, name='detail'),
    path('<str:product_pk>/edit/', views.edit_product, name='edit'),
    path('<str:product_pk>/delete/', views.product_delete, name='delete'),
]