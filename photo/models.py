from django.db import models
from django.forms import ValidationError

class User(models.Model):

    email = models.TextField(primary_key=True)
    name_first = models.TextField(blank=True, null=True)
    name_last = models.TextField(blank=True, null=True)
    profile_picture = models.ForeignKey(
        "Picture",
        on_delete=models.SET_NULL,
        related_name="user_picture_path",
        null=True,
    )
    profile_picture_updated_at = models.DateTimeField(null=True)
    user_handle = models.TextField(unique=True, null=True)

    def validate_profile_picture(self):
        if self.profile_picture.user.email != self.email:
            raise ValidationError(
                "The user's profile picture must be owned by the same user."
            )

    def save(self, *args, **kwargs):
        self.validate_profile_picture()
        super(ContestSubmission, self).save(*args, **kwargs)


class Picture(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="picture_user"
    )
    picture_path = models.TextField(primary_key=True)
    likes = models.ManyToManyField(User, related_name="picture_likes")


class PictureComment(models.Model):
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
    )
    picture = models.ForeignKey(
        "Picture",
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Collection(models.Model):
    name = models.TextField(null=True)
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
    )
    pictures = models.ManyToManyField(Picture, related_name="collection_pictures")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "user"], name="collection_pk")
        ]


class Contest(models.Model):
    title = models.TextField(null=True)
    description = models.TextField()
    cover_picture = models.ForeignKey(
        "Picture",
        on_delete=models.SET_NULL,
        null=True,
    )
    prize = models.TextField(null=True)
    automated_dates = models.BooleanField(default=True)
    upload_phase_start = models.DateTimeField(auto_now_add=True)
    upload_phase_end = models.DateTimeField(null=True)
    voting_phase_end = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)
    winners = models.ManyToManyField(User, related_name="contest_winners")
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        related_name="contest_created_by",
        null=True,
    )

    def validate_user(self):
        qs = User.objects.filter(email=self.created_by.email)
        if qs.exists():
            raise ValidationError(
                "The contest must be created by a valid user (created_by can not be null)."
            )

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.validate_user()
        super(ContestSubmission, self).save(*args, **kwargs)


class ContestSubmission(models.Model):
    contest = models.ForeignKey(
        "Contest",
        on_delete=models.CASCADE,
    )
    picture = models.ForeignKey(
        "Picture",
        on_delete=models.CASCADE,
    )
    submissionDate = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(User, related_name="submission_votes")

    def validate_unique(self):
        qs = ContestSubmission.objects.filter(picture__user=self.picture.user)
        if qs.exists():
            raise ValidationError("Each user can only submit one picture per contest")

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(ContestSubmission, self).save(*args, **kwargs)
