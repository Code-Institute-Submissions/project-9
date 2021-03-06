from django.test import TestCase
from .views import index

# This test checks if the homepoage loads or not
class TestViews(TestCase):

    def test_get_home_page(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "index.html")