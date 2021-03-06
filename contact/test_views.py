from django.test import TestCase
from .views import contact

# This test checks of the page loads or not
class TestViews(TestCase):

    def test_get_contact_page(self):
        page = self.client.get("/contact/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "contact.html")