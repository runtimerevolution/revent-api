from django.contrib import admin, messages
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin

from photo.fixtures import (
    DRAW_PHASE_NOT_SET,
    UPLOAD_PHASE_NOT_OVER,
    VOTING_PHASE_NOT_OVER,
)
from photo.models import (
    Collection,
    Contest,
    ContestSubmission,
    Picture,
    PictureComment,
    User,
)
from utils.enums import ContestInternalStates


@admin.register(User)
class UserAdmin(UserAdmin):
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

    actions = [
        "close_contest",
    ]

    def close_contest(self, request, queryset):
        for contest in queryset:
            if contest.voting_phase_end and contest.voting_phase_end > timezone.now():
                messages.info(request, VOTING_PHASE_NOT_OVER)
                break

            if (
                contest.upload_phase_end
                and contest.upload_phase_end > timezone.now()
                or not contest.upload_phase_end
            ):
                messages.info(request, UPLOAD_PHASE_NOT_OVER)
                break

            contest.close_contest()
            if contest.internal_status == ContestInternalStates.DRAW:
                contest.upload_phase_end = ""
                messages.info(request, DRAW_PHASE_NOT_SET)


@admin.register(PictureComment)
class PictureCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "picture", "text", "created_at")


@admin.register(ContestSubmission)
class ContestSubmissionAdmin(admin.ModelAdmin):
    list_display = ("contest", "picture", "submission_date", "contest_status")

    @admin.display(ordering="-contest__internal_status")
    def contest_status(self, obj):
        return obj.contest.internal_status
