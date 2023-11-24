from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from .models import Product, Category

# Create your tests here.

class ProductViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='abcdABCD1234')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            category = self.category,
            name = 'Test Product',
            price = 100,
            created_by = self.user
        )




    def test_product_detail_view(self):
        response = self.client.get(reverse('product:detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
    
        product = Product.objects.get(id=self.product.id)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 100)




    def test_new_product_view(self):
        self.client.login(username='testuser', password='abcdABCD1234')
        response = self.client.post(reverse('product:new'), data={
            'category': self.category.id,
            'name': 'New Product',
            'price': 200,
            
        })
        self.assertEqual(response.status_code, 302)

        new_product = Product.objects.get(name='New Product')
        self.assertEqual(new_product.name, 'New Product')
        self.assertEqual(new_product.price, 200)




    def test_edit_product_view(self):
        self.client.login(username='testuser', password='abcdABCD1234')
        response = self.client.post(reverse('product:edit', args=[self.product.id]), data={
            'category': self.category.id,
            'name': 'Updated Product',
            'price': 150
        })

        updated_product = Product.objects.get(id=self.product.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_product.name, 'Updated Product')
        self.assertEqual(updated_product.price, 150)




    def test_product_delete_view(self):
        self.client.login(username='testuser', password='abcdABCD1234')
        response = self.client.post(reverse('product:delete', args=[self.product.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.filter(id=self.product.id).count(), 0)

