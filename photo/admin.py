from ast import Sub
from django.contrib import admin
from .models import User, Contest, Submission, Vote, Comment, Result


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    pass


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass
