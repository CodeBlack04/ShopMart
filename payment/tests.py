from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from product.models import Product, Category

from django.conf import settings
from unittest.mock import patch, MagicMock


class PaymentViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='abcdABCD1234')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            category = self.category,
            name = 'Test Product',
            price = 100,
            created_by = self.user
        )

    
    def test_stripe_config_view(self):
        response = self.client.get(reverse('payment:config'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'publicKey': settings.STRIPE_PUBLISHABLE_KEY})


    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session_view(self, mock_create_session):
        mock_checkout_session = MagicMock(id='fake_session_id')
        mock_create_session.return_value = mock_checkout_session

        self.client.login(username='testuser', password='abcdABCD1234')

        response = self.client.get(reverse('payment:checkout', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

        mock_create_session.assert_called_once_with(
            client_reference_id=self.product.pk,
            success_url='http://127.0.0.1:8000/payment/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/payment/cancelled/',
            payment_method_types=['card'],
            mode='payment',
            line_items=[{
                "price_data": {
                    "currency": 'usd',
                    "product_data": {"name": self.product.name,},
                    "unit_amount": int(self.product.price * 100),
                },
                "quantity": 1,
            }]
        )

        

