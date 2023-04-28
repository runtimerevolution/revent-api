from django.contrib import admin
from django.urls import path
from strawberry.django.views import AsyncGraphQLView

from photo.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", AsyncGraphQLView.as_view(schema=schema)),
]
