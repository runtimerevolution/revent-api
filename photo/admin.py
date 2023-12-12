from django.contrib import admin

from photo.models import (
    Collection,
    Contest,
    ContestSubmission,
    Picture,
    PictureComment,
    User,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "name_first",
        "name_last",
        "profile_picture",
        "profile_picture_updated_at",
        "user_handle",
    )

    ordering = ["email"]


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ("user", "file")


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "user")


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "prize",
        "upload_phase_start",
        "upload_phase_end",
        "voting_phase_end",
    )


@admin.register(PictureComment)
class PictureCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "picture", "text", "created_at")


@admin.register(ContestSubmission)
class ContestSubmissionAdmin(admin.ModelAdmin):
    list_display = ("contest", "picture", "submission_date")
