from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers
from photo import views
from photo.views import UserViewSet, exchange_token

api_router = routers.DefaultRouter()
api_router.register(r"users", UserViewSet, basename="users")
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_router.urls)),
    path("api/auth/token/exchange/", exchange_token, name="token-exchange"),
    # path("", views.hello, name="hello"),
    path("photo/", include("photo.urls")),
]
