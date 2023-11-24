from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from product.models import Product, Category
from .forms import CategoryForm

# Create your tests here.
class ProductsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='abcdABCD1234')

        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')

        self.product1 = Product.objects.create(
            category=self.category1,
            name='Product 1',
            price=100,
            created_by = self.user
        )

        self.product2 = Product.objects.create(
            category=self.category2,
            name='Product 2',
            price=150,
            created_by = self.user
        )

    def test_get_products_view(self):
        response_without_query = self.client.get(reverse('browse:index'))

        self.assertEqual(response_without_query.status_code, 200)
        self.assertContains(response_without_query, 'Product 1')
        self.assertContains(response_without_query, 'Product 2')
        self.assertContains(response_without_query, 'Category 1')
        self.assertContains(response_without_query, 'Category 2')

        self.assertIsInstance(response_without_query.context['category_form'], CategoryForm)

        products = response_without_query.context['products']

        self.assertEqual(len(products), 2)
        self.assertEqual(products[0].name, 'Product 1')
        self.assertEqual(products[1].name, 'Product 2')

        response_with_query = self.client.get(reverse('browse:index') + '?query=Product 1')
        self.assertEqual(len(response_with_query.context['products']), 1)
        self.assertEqual(response_with_query.context['products'][0].name, 'Product 1')

        response_with_max_price = self.client.get(reverse('browse:index') + '?max-price=125')
        self.assertEqual(len(response_with_max_price.context['products']), 1)
        self.assertEqual(response_with_max_price.context['products'][0].name, 'Product 1')

        response_with_categories = self.client.get(reverse('browse:index') + f'?categories={self.category2.id}')
        self.assertEqual(len(response_with_categories.context['products']), 1)
        self.assertEqual(response_with_categories.context['products'][0].name, 'Product 2')

        response_with_all_filters = self.client.get(reverse('browse:index') + '?query=Product 1' + '&max-price=125' + f'&categories={self.category1.id}')
        self.assertEqual(len(response_with_all_filters.context['products']), 1)
        self.assertEqual(response_with_all_filters.context['products'][0].name, 'Product 1')