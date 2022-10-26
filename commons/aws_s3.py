import boto3
from botocore.exceptions import ClientError
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class awsS3:
    def __init__(self):
        self.s3 = boto3.resource("s3", endpoint_url=settings.AWS_S3_HOST)
        self.create_bucket(settings.AWS_S3_BUCKET)

    def list_buckets(self):
        return self.s3.meta.client.list_buckets()

    def create_bucket(self, name):
        list_buckets = self.list_buckets().get("Buckets")
        buckets_found = [bucket for bucket in list_buckets if bucket.get("Name") == settings.AWS_S3_BUCKET]
        if len(buckets_found) == 0:
            self.s3.meta.client.create_bucket(
                Bucket=name, CreateBucketConfiguration={"LocationConstraint": "eu-west-1"}
            )

    # For binary files
    def upload_file_obj(self, file, mykey):
        self.s3.meta.client.upload_fileobj(file, settings.AWS_S3_BUCKET, mykey)

    # For binary files
    def get_file_obj(self, obj_key):
        return self.s3.meta.client.get_object(Bucket=settings.AWS_S3_BUCKET, Key=obj_key)

    def list_objs(self):
        return self.s3.meta.client.list_objects(Bucket=settings.AWS_S3_BUCKET)

    # For non binary files; requires path for the file
    def upload_file(self, file, description):
        self.s3.meta.client.upload_file(file, settings.AWS_S3_BUCKET, description)

    # For non binary files; requires path for the file
    def download_file(self, path, name):
        self.s3.meta.client.download_file(settings.AWS_S3_BUCKET, name, path)

    def get_name(self):
        return settings.AWS_S3_BUCKET
