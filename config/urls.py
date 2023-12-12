from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from photo.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema))),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.social.urls")),
]
