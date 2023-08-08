from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class URLTests(TestCase):
    def test_testhomepage(self):
        self.user = User.objects.create_user('test_user_3', 'randumbguy21@gmail.com', 'test_user_3_password')
        self.client.login(username='test_user_3', password='test_user_3_password')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_monitorpage(self):
        self.user = User.objects.create_user('test_user_3', 'randumbguy21@gmail.com', 'test_user_3_password')
        self.client.login(username='test_user_3', password='test_user_3_password')
        response = self.client.get(reverse('monitor'))
        self.assertEqual(response.status_code, 200)