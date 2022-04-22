from django.contrib import admin
from django.urls import path
from photo import views
from photo.schema import schema
from strawberry.django.views import AsyncGraphQLView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/graphql/", AsyncGraphQLView.as_view(schema=schema))
    # In case we wanna have multiple url files for each app
    # path('photo/', include('photo.urls'))
]
