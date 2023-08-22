import boto3

s3 = boto3.resource("s3", endpoint_url="http://localhost:4566")
s3.create_bucket(Bucket="pictures")
