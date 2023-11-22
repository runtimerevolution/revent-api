from django.core.exceptions import ValidationError

from django.http import HttpResponse
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class AuthenticatonMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        return HttpResponse(exception)

    def process_view(self, request, view_func, view_args, view_kwargs):
        JWT_authenticator = JWTAuthentication()
        try:
            if response := JWT_authenticator.authenticate(request):
                user, token = response
                request.user = user
        except (ValidationError, InvalidToken):
            return HttpResponse("Invalid Token", status=status.HTTP_406_NOT_ACCEPTABLE)
