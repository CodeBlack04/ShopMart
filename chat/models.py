from django.db import models
from django.contrib.auth.models import User
from product.models import Product

import uuid

# Create your models here.

class Message(models.Model):
    body = models.TextField()
    sent_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.sent_by}-{self.body}'
    
    class Meta:
        ordering = ('created_at',)

class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    product = models.ForeignKey(Product, related_name='chatrooms', blank=True, null=True, on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message, blank=True)
    members = models.ManyToManyField(User, related_name='chatrooms')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.product.name}-{self.id}'
    
    class Meta:
        ordering = ('-created_at',)