from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from photo.schema import schema
from photo.views import ReventGraphQLView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(ReventGraphQLView.as_view(schema=schema))),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.social.urls")),
]
