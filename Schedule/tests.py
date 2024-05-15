from django.test import TestCase, SimpleTestCase

# Create your tests here.
class SimpleTests(SimpleTestCase):
    def test_schedule_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
