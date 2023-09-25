import boto3
from django.conf import settings

s3 = boto3.client("s3", endpoint_url=settings.AWS_S3_ENDPOINT_URL)

s3.create_bucket(
    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
    CreateBucketConfiguration={"LocationConstraint": settings.AWS_DEFAULT_REGION},
)
s3.list_buckets()
