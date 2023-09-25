from django.contrib import admin

from photo.models import (
    User,
    Collection,
    Contest,
    Picture,
    PictureComment,
    ContestSubmission,
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
    pass


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    pass


@admin.register(PictureComment)
class PictureCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(ContestSubmission)
class ContestSubmissionAdmin(admin.ModelAdmin):
    pass
