from django.urls import reverse
from django.test import TestCase, Client


class BaseViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        
    def test_that_200_is_thrown_for_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_that_200_is_thrown_for_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_that_200_is_thrown_for_help(self):
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, 200)
