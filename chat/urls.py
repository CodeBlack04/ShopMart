from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),

    path('<str:chatroom_pk>/', views.chatroom, name='chatroom'),

    path('new/<str:product_pk>/', views.new_chatroom, name='new-chatroom'),
]