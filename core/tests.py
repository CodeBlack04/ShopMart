from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from product.models import Product, Category

# Create your tests here.
class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='abcdABCD1234')
        self.category = Category.objects.create(name='Test Category')


    def test_dashboard_view(self):
        self.client.login(username='testuser', password='abcdABCD1234')

        product1 = Product.objects.create(
            category=self.category,  # Replace with the correct category
            name='Product 1',
            price=100.0,
            created_by = self.user
        )

        product2 = Product.objects.create(
            category=self.category,
            name='Product 2',
            price=200.0,
            created_by = self.user
        )

        response = self.client.get(reverse('core:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')
        self.assertIn(product1, response.context['products'])
        self.assertIn(product2, response.context['products'])

        returned_products = Product.objects.all()

        for product in returned_products:
            self.assertEqual(product.created_by, self.user)


    def test_index_view(self):
        product1 = Product.objects.create(
            category=self.category,  # Replace with the correct category
            name='Product 1',
            price=100.0,
            created_by = self.user
        )

        product2 = Product.objects.create(
            category=self.category,
            name='Product 2',
            price=200.0,
            created_by = self.user
        )

        response = self.client.get(reverse('core:index'))

        self.assertEqual(response.status_code, 200)

        products = Product.objects.all()

        self.assertTrue(products.exists())
        self.assertEqual(products.count(), 2)


    def test_contact_view(self):
        post_response = self.client.post(reverse('core:contact'), data={
            'full_name': 'test',
            'email': 'test@test.com',
            'subject': 'test'
        })

        get_response = self.client.get(reverse('core:contact'))

        self.assertEqual(post_response.status_code, 302)
        self.assertEqual(get_response.status_code, 200)