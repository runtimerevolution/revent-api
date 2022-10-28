from PIL import Image
from django.utils import timezone
from django.db import models
import uuid
import boto3
from botocore.exceptions import ClientError
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from commons.aws_s3 import awsS3
from django.core.files.uploadedfile import SimpleUploadedFile


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
    updated_by = models.UUIDField(("updated by"), null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.created_by == None:
            self.created_by = kwargs.get("user")
        else:
            self.updated_by = kwargs.get("user")
        super(AuthorChangesMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class SubmissionContentStorage(S3Boto3Storage):
    bucket_name = "submissionimages"


def upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<brand_id>/logo.png
    return f"{instance.id}/{filename}"


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
    url = models.ImageField(storage=SubmissionContentStorage, null=True, blank=True, upload_to=upload_path)
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
