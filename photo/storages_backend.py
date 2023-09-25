from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    bucket_name = "revent-media"


def picture_path(instance, filename):
    return "pictures/{0}/{1}".format(instance.user.email, filename)
