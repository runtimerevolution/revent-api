from django.contrib import admin
from django.urls import path
from strawberry.django.views import AsyncGraphQLView
from photo.schema import schema

from photo import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.hello, name="hello"),
    path("api/graphql/", AsyncGraphQLView.as_view(schema=schema))
    # In case we wanna have multiple url files for each app
    # path('photo/', include('photo.urls'))
]
