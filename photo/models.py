import uuid
from django.db import models
from django.forms import ValidationError
from django.utils import timezone

from photo.storages_backend import PublicMediaStorage, picture_path


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.TextField(unique=True)
    name_first = models.TextField(blank=True, null=True)
    name_last = models.TextField(blank=True, null=True)
    profile_picture = models.ForeignKey(
        "Picture",
        on_delete=models.SET_NULL,
        related_name="user_picture",
        blank=True,
        null=True,
    )
    profile_picture_updated_at = models.DateTimeField(blank=True, null=True)
    user_handle = models.TextField(unique=True, null=True)

    def validate_profile_picture(self):
        if not self._state.adding:
            old_picture = User.objects.filter(email=self.email).first().profile_picture
            if old_picture and self.profile_picture.id != old_picture.id:
                self.profile_picture_updated_at = timezone.now()
        if self.profile_picture and self.profile_picture.user.email != self.email:
            raise ValidationError(
                "The user's profile picture must be owned by the same user."
            )

    def save(self, *args, **kwargs):
        self.validate_profile_picture()
        super(User, self).save(*args, **kwargs)


class Picture(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="picture_user", to_field="id"
    )
    picture_path = models.FileField(
        storage=PublicMediaStorage(),
        upload_to=picture_path,
    )
    likes = models.ManyToManyField(User, related_name="picture_likes")


class PictureComment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, to_field="id")
    picture = models.ForeignKey(
        "Picture",
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Collection(models.Model):
    name = models.TextField()
    user = models.ForeignKey("User", on_delete=models.CASCADE, to_field="id")
    pictures = models.ManyToManyField(Picture, related_name="collection_pictures")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "user"], name="collection_pk")
        ]


class Contest(models.Model):
    title = models.TextField()
    description = models.TextField()
    cover_picture = models.ForeignKey(
        "Picture",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    prize = models.TextField()
    automated_dates = models.BooleanField(default=True)
    upload_phase_start = models.DateTimeField(default=timezone.now)
    upload_phase_end = models.DateTimeField(null=True, blank=True)
    voting_phase_end = models.DateTimeField(null=True, blank=True)
    winners = models.ManyToManyField(User, related_name="contest_winners")
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        related_name="contest_created_by",
        blank=True,
        null=True,
        to_field="id",
    )

    def validate_user(self):
        if not (
            self.created_by
            and User.objects.filter(email=self.created_by.email).exists()
        ):
            raise ValidationError(
                "The contest must be created by a valid user (created_by can not be null)."
            )

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.validate_user()
        super(Contest, self).save(*args, **kwargs)


class ContestSubmission(models.Model):
    contest = models.ForeignKey(
        "Contest",
        on_delete=models.CASCADE,
    )
    picture = models.ForeignKey(
        "Picture",
        on_delete=models.CASCADE,
    )
    submission_date = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(User, related_name="submission_votes")

    def validate_unique(self, *args, **kwargs):
        qs = ContestSubmission.objects.filter(
            contest=self.contest, picture__user=self.picture.user
        )
        if qs.exists() and self._state.adding:
            raise ValidationError("Each user can only submit one picture per contest")

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(ContestSubmission, self).save(*args, **kwargs)
