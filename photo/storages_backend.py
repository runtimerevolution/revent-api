from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    custom_domain = "{0}/{1}".format("localhost:4566", "revent-media")
