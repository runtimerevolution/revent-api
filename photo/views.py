from django.views import View
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import login
from config import settings
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class GoogleLogin(
    SocialLoginView
):  # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.BASE_APP_URL
    client_class = OAuth2Client
