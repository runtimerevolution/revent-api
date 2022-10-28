from django.contrib import admin
from .models import User, Contest, Submission, Vote, Comment, Result


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ("id", "email", "first_name", "last_name", "date_joined")
    search_fields = ("email",)


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):

    list_display = ("name", "description", "date_start", "date_end")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "contest", "url", "description")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "submission", "text")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "submission", "value")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("contest", "submission", "position")
