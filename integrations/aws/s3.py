import boto3
import botocore
from django.conf import settings


class Client:
    def __init__(self) -> None:
        self.s3 = boto3.client("s3", endpoint_url=settings.AWS_S3_ENDPOINT_URL)

    def create_bucket(
        self,
        bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
        location=settings.AWS_DEFAULT_REGION,
    ):
        if not self.check_bucket_existence(bucket_name):
            return self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": location},
            )

    def check_bucket_existence(self, bucket_name):
        try:
            self.s3.head_bucket(Bucket=bucket_name)
            return True
        except botocore.exceptions.ClientError:
            return False

    def delete_bucket(self, bucket_name):
        return self.s3.delete_bucket(Bucket=bucket_name)

    def list_bucket(self):
        return self.s3.list_buckets()

    def get_object(self, bucket, key):
        return self.s3.get_object(Bucket=bucket, Key=key)

    def delete_object(self, bucket, key):
        return self.s3.delete_object(Bucket=bucket, Key=key)
