from django.urls import path
from photo import views

urlpatterns = [
    path("submissions/", views.SubmissionList.as_view()),
    path("submissions/<uuid:id>/", views.SubmissionDetail.as_view()),
    path("users/", views.UserList.as_view()),
    path("users/<uuid:id>/", views.UserDetail.as_view()),
    path("contests/", views.ContestList.as_view()),
    path("contests/<uuid:id>/", views.submissions_from_contest, name="submissions-from-contest"),
]
