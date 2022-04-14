from django.utils import timezone
from django.db import models
import uuid


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class User(UUIDModel):
    email = models.EmailField(("email address"), unique=True)
    date_joined = models.DateTimeField(("date joined"), default=timezone.now)
    first_name = models.TextField(("First Name"), blank=True, null=True)
    last_name = models.TextField(("Last Name"), blank=True, null=True)


class Contest(UUIDModel):
    date_start = models.DateField(auto_now_add=True)
    date_end = models.DateField()
    name = models.TextField()
    description = models.TextField(blank=True, null=True)


class Submission(UUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    content = models.TextField()  # unique=True?
    description = models.TextField(blank=True, null=True)  # max_length?


class Comment(UUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
    )
    text = models.TextField()  # max_length?


class Vote(UUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    value = models.IntegerField()


class Result(UUIDModel):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
