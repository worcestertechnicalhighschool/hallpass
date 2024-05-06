from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Student, HallPass, Destination, Profile, Building, Category

# class URLTests(TestCase):
#     def test_testhomepage(self):
#         self.user = User.objects.create_user('test_user_3', 'randumbguy21@gmail.com', 'test_user_3_password')
#         self.client.login(username='test_user_3', password='test_user_3_password')
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
    
#     def test_monitorpage(self):
#         self.user = User.objects.create_user('test_user_3', 'randumbguy21@gmail.com', 'test_user_3_password')
#         self.client.login(username='test_user_3', password='test_user_3_password')
#         response = self.client.get(reverse('monitor'))
#         self.assertEqual(response.status_code, 200)

from datetime import datetime, timedelta
class HallPassTests(TestCase):
    def setUp(self):
        self.building = Building.objects.create(building = 'test_building')
        self.user = User.objects.create_user('test_user_3', 'randumbguy21@gmail.com', 'test_user_3_password')
        self.student = Student.objects.create(first_name = 'Test', last_name = 'Student', student_id = '111111', building = self.building)
        self.category = Category.objects.create(name = 'boys')
        self.br = Destination.objects.create(room = "testBR", building = self.building, category = self.category, max_people_allowed = 2)

    def test_timein(self):
        testpass = HallPass.objects.create(student_id = self.student, destination = self.br, user = self.user, time_in = datetime.now())   
        self.assertTrue(testpass.time_in)