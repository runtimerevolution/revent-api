import boto3
from botocore.exceptions import ClientError
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class awsS3:
    def create_aws_client(self):
        return boto3.resource("s3", endpoint_url=settings.AWS_S3_HOST)

    # For binary files
    def upload_file_obj(self, file, mykey):
        s3 = self.create_aws_client()
        s3.meta.client.upload_fileobj(file, settings.AWS_S3_BUCKET, mykey)

    # For binary files
    def get_file_obj(self, obj_key):
        s3 = self.create_aws_client()
        return s3.meta.client.get_object(Bucket=settings.AWS_S3_BUCKET, Key=obj_key)

    def list_objs(self):
        s3 = self.create_aws_client()
        return s3.meta.client.list_objects(Bucket=settings.AWS_S3_BUCKET)

    # For non binary files; requires path for the file
    def upload_file(self, file, description):
        s3 = self.create_aws_client()
        s3.meta.client.upload_file(file, settings.AWS_S3_BUCKET, description)

    # For non binary files; requires path for the file
    def download_file(self, path, name):
        s3 = self.create_aws_client()
        s3.meta.client.download_file(settings.AWS_S3_BUCKET, name, path)
