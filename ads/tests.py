from django.test import TestCase

# Create your tests here.

from django.contrib import auth

from ads.models import User


class AuthTestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create_user('peter', 'test@dom.com', '123')
        self.u.is_staff = True
        self.u.is_superuser = True
        self.u.is_active = True
        self.u.save()

    def testLogin(self):
        self.client.login(username='peter', password='123')