from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from product.models import Category, Product
from chat.models import ChatRoom, Message

# Create your tests here.

class ChatViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='abcdABCD1234')
        self.customer = User.objects.create_user(username='customer', password='abcdABCD1234')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            category = self.category,
            name = 'Test Product',
            price = 100,
            created_by = self.user
        )

    
    def test_new_chatroom_view(self):
        self.client.login(username='customer', password='abcdABCD1234')

        chatrooms = ChatRoom.objects.all()
        self.assertFalse(chatrooms.exists())
        self.assertEqual(chatrooms.count(), 0)

        response = self.client.post(reverse('chat:new-chatroom', args=[self.product.id]), data={
            'body': 'Hello!'
        })

        chatrooms = ChatRoom.objects.all()
        message = chatrooms.first().messages.first().body
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(chatrooms.exists)
        self.assertEqual(chatrooms.count(), 1)
        self.assertEqual(message, 'Hello!')


    def test_chatroom_view(self):
        self.client.login(username='customer', password='abcdABCD1234')

        message1 = Message.objects.create(
            body = 'Hello!',
            sent_by = self.customer
        )

        message2 = Message.objects.create(
            body = 'Hi! There!',
            sent_by = self.user
        )

        chatroom = ChatRoom.objects.create(
            product = self.product
        )
        chatroom.members.add(self.customer)
        chatroom.members.add(self.user)
        chatroom.messages.add(message1)
        chatroom.messages.add(message2)

        response = self.client.get(reverse('chat:chatroom', args=[chatroom.id]))

        self.assertEqual(response.status_code, 200)

        messages = chatroom.messages.all()

        self.assertEqual(messages.first().body, 'Hello!')
        self.assertEqual(messages.last().body, 'Hi! There!')
        self.assertEqual(messages.first().sent_by, self.customer)
        self.assertEqual(messages.last().sent_by, self.user)

    
    def test_inbox_view(self):
        self.client.login(username='customer', password='abcdABCD1234')

        message1 = Message.objects.create(
            body = 'Hello!',
            sent_by = self.customer
        )

        message2 = Message.objects.create(
            body = 'Hi! There!',
            sent_by = self.user
        )

        chatroom = ChatRoom.objects.create(
            product = self.product
        )
        chatroom.members.add(self.customer)
        chatroom.members.add(self.user)
        chatroom.messages.add(message1)
        chatroom.messages.add(message2)

        response = self.client.get(reverse('chat:inbox'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ChatRoom.objects.all().exists())
        self.assertEqual(ChatRoom.objects.all().count(), 1)
        
