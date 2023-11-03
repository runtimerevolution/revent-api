import uuid

from django.db import models
from django.forms import ValidationError
from django.utils import timezone

from photo.fixtures import (
    OUTDATED_SUBMISSION_ERROR_MESSAGE,
    REPEATED_VOTE_ERROR_MESSAGE,
    UNIQUE_SUBMISSION_ERROR_MESSAGE,
    VALID_USER_ERROR_MESSAGE,
)
from photo.manager import SoftDeleteManager
from photo.storages_backend import PublicMediaStorage, picture_path


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class User(SoftDeleteModel):
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(is_deleted="False"),
                name="user_email",
            )
        ]

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


class Picture(SoftDeleteModel):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="picture_user"
    )
    name = models.TextField(blank=True, null=True)
    file = models.ImageField(
        storage=PublicMediaStorage(),
        upload_to=picture_path,
    )
    likes = models.ManyToManyField(User, related_name="picture_likes")

    def like_picture(self, user):
        if user not in self.likes.filter(id=user):
            self.likes.add(user)
            self.save()
        return self


class PictureComment(SoftDeleteModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    picture = models.ForeignKey(
        "Picture",
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Collection(SoftDeleteModel):
    name = models.TextField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    pictures = models.ManyToManyField(Picture, related_name="collection_pictures")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "user"], name="collection_pk")
        ]

    def add_picture(self, picture):
        if picture not in self.pictures.filter(id=picture):
            self.pictures.add(picture)
            self.save()
        return self


class Contest(SoftDeleteModel):
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
    )

    def validate_user(self):
        if not (
            self.created_by
            and User.objects.filter(email=self.created_by.email).exists()
        ):
            raise ValidationError(VALID_USER_ERROR_MESSAGE)

    def close_contest(self):
        self.voting_phase_end = timezone.now()
        self.save()
        return self

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.validate_user()
        super(Contest, self).save(*args, **kwargs)


class ContestSubmission(SoftDeleteModel):
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
            raise ValidationError(UNIQUE_SUBMISSION_ERROR_MESSAGE)

    def validate_vote(self):
        user_vote = ContestSubmission.objects.filter(
            contest=self.contest, votes=self.picture.user
        )

        if user_vote.exists() and self._state.adding:
            raise ValidationError(REPEATED_VOTE_ERROR_MESSAGE)

    def validate_submission_date(self):
        if self.contest.upload_phase_end is not None and (
            not (
                self.contest.upload_phase_start
                <= self.submission_date
                <= self.contest.upload_phase_end
            )
        ):
            raise ValidationError(OUTDATED_SUBMISSION_ERROR_MESSAGE)

    def save(self, *args, **kwargs):
        self.validate_unique()
        self.validate_vote()
        self.validate_submission_date()
        super(ContestSubmission, self).save(*args, **kwargs)

    def add_vote(self, user):
        if user not in self.votes.filter(id=user):
            self.votes.add(user)
            self.save()
        return self
