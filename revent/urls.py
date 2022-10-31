from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers

from photo.views import UserViewSet, SubmissionViewSet, ContestViewSet
from photo import views

api_router = routers.DefaultRouter()
api_router.register(r"users", UserViewSet, basename="users")
api_router.register(r"submissions", SubmissionViewSet, basename="submissions")
api_router.register(r"contests", ContestViewSet, basename="contests")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_router.urls)),
]
