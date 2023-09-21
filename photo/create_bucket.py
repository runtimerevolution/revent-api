import boto3

s3 = boto3.client("s3", endpoint_url="http://localhost.localstack.cloud:4566")

s3.create_bucket(
    Bucket="revent-media", CreateBucketConfiguration={"LocationConstraint": "us-west-1"}
)
s3.list_buckets()
