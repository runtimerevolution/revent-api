from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from photo.schema import schema
from photo.views import GoogleLogin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema))),
    path("accounts/", include("allauth.urls")),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
]
