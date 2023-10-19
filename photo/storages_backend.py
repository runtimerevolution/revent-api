from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME


def picture_path(instance, filename):
    return "media/{0}/{1}.webp".format(instance.user.id, filename)
