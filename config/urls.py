from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from photo.schema import schema
from photo.views import GoogleLoginApi, GoogleLoginRedirectApi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema))),
    path(
        "auth/google/",
        GoogleLoginRedirectApi.as_view(),
    ),
    path("auth/login/callback/", GoogleLoginApi.as_view()),
]
