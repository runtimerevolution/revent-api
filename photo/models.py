from django.db import models
from django.forms import ValidationError


# Create your models here.
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
    pictures = models.ManyToManyField(Picture)

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
    votes = models.ManyToManyField(User)

    def validate_unique(self):
        qs = ContestSubmission.objects.filter(picture__user=self.picture.user)
        if qs.exists():
            raise ValidationError("Each user can only submit one picture per contest")

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(ContestSubmission, self).save(*args, **kwargs)
