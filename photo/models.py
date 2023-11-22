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

from photo.storages_backend import PublicMediaStorage, picture_path
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_super_user(
        self, email, password, **extra_fields
    ):  # sourcery skip: raise-from-previous-error
        """
        Creates and saves a User with the given email.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, request, data, **extra_fields):
        data["is_staff"] = False
        data["is_superuser"] = False
        data["is_active"] = False
        return self._create_user(request, data)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_super_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.TextField(unique=True)
    username = models.CharField("username", max_length=150, null=True)
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

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

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
        "User", on_delete=models.CASCADE, related_name="picture_user"
    )
    name = models.TextField(blank=True, null=True)
    file = models.FileField(
        storage=PublicMediaStorage(),
        upload_to=picture_path,
    )
    likes = models.ManyToManyField(User, related_name="picture_likes")


class PictureComment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    picture = models.ForeignKey(
        "Picture",
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Collection(models.Model):
    name = models.TextField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)
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
    )

    def validate_user(self):
        if not (
            self.created_by
            and User.objects.filter(email=self.created_by.email).exists()
        ):
            raise ValidationError(VALID_USER_ERROR_MESSAGE)

    def close_contest(self):
        self.voting_phase_end = timezone.now()
        return self

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
