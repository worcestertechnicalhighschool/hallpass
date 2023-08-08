from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Student, HallPass, Destination, Profile, Building
from .forms import CreateHallPassForm

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

from datetime import datetime, timedelta
class HallPassTests(TestCase):
    def test_timeout(self):
        self.user = User.objects.create_user('test_user_3', 'randumbguy21@gmail.com', 'test_user_3_password')
        testStudent = Student('Test','Student','111111')
        testBR = Destination('TestBr')
        TestHallPass = HallPass(Time_in = datetime.now(),Time_out =  (datetime.now() + timedelta(minutes = 30)),student_id = testStudent ,destination = testBR,user = self.user)
        self.assertEqual(TestHallPass.Time_out > TestHallPass.Time_in, True)

    def test_profile_location(self):
        self.user = User.objects.create_user('test_user_3', 'randumbguy21@gmail.com', 'test_user_3_password')
        testHS = Building('WTHS')
        testStudent = Student('Test','Student','111111')
        testBR = Destination(building = testHS,room = 'WTHS')
        testProfile = Profile(user = self.user,building = testHS)
        TestHallPass = HallPass(Time_in = datetime.now(),Time_out = (datetime.now() + timedelta(minutes = 30)),student_id = testStudent ,destination = testBR,user = testProfile.user)
        self.assertEqual(TestHallPass.user, False)