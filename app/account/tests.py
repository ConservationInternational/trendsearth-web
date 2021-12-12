from django.test import TestCase

# Create your tests here.

from utils.api import Api
from utils.conf import *


class ApiTestCase(TestCase):
    def test_api_login(self):
        username = "robertohuru@gmail.com"
        password = "EJAIFO85P7NXPL6ZG6IJ"

        api = Api(email=username, password=password)
        self.assertEqual(1, 0)
