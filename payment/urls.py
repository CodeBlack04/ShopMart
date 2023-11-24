from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('config/', views.stripe_config, name='config'),
    path('create-checkout-session/<str:product_pk>/', views.create_checkout_session, name='checkout'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancelled/', views.CancelledView.as_view(), name='cancelled'),
    path('webhook/', views.stripe_webhook, name='webhook'),
]