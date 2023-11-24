from django.test import TestCase

from django.urls import reverse

# Create your tests here.
class SignupViewTest(TestCase):
    def test_signup_view(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'abcdABCD1234',
            'password2': 'abcdABCD1234'
        }

        post_response = self.client.post(reverse('myauth:signup'), data=form_data)

        get_response = self.client.get(reverse('myauth:signup'))

        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, reverse('core:index'))
        self.assertEqual(get_response.status_code, 200)