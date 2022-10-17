from django.utils import timezone
from django.db import models
import uuid


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class TimestampsMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True


class AuthorChangesMixin(models.Model):
    created_by = models.UUIDField(("created by"))
    updated_by = models.UUIDField(("updated by"))

    def save(self, *args, **kwargs):
        if self.created_by == None:
            self.created_by = kwargs.get("user")
        else:
            self.updated_by = kwargs.get("user")
        super(AuthorChangesMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class User(UUIDModel, TimestampsMixin):
    email = models.EmailField(("email address"), unique=True)
    date_joined = models.DateTimeField(("date joined"), default=timezone.now)
    first_name = models.TextField(("First Name"))
    last_name = models.TextField(("Last Name"))


class Contest(UUIDModel, TimestampsMixin, AuthorChangesMixin):
    date_start = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField()
    name = models.TextField()
    description = models.TextField()


class Submission(UUIDModel, TimestampsMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    content = models.TextField()
    description = models.TextField()


class Comment(UUIDModel, TimestampsMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
    )
    text = models.TextField()


class Vote(UUIDModel, TimestampsMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    value = models.IntegerField()


class Result(UUIDModel):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
