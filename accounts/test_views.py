from django.test import TestCase
from .views import profile, login, update_profile
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import Profile

# this test checks if the login page loads or not
class TestViews(TestCase):

    def test_get_login_page(self):
        page = self.client.get("/accounts/login/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "login.html")    
    
class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('register')
        
class RegisterTest(BaseTest):
    def test_can_view_registration_page(self):
        response=self.client.get(reverse("register"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, "registration.html")
        