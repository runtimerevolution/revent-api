import vcr
import urllib.request
from django.test import TestCase


class AuthTest(TestCase):
    @vcr.use_cassette()
    def test_google_auth(self):
        response = urllib.request.urlopen(
            "http://127.0.0.1:8000/auth/google-redirect/"
        ).read()
        assert response.status_code == 200
