from django.urls import path
from . import views

app_name = 'browse'

urlpatterns = [
    path('', views.get_products, name='index'),
]