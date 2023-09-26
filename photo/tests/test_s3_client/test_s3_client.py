import botocore
from django.test import TestCase

from integrations.aws.s3 import Client


class S3BucketTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()

    def test_s3(self):
        response_create = self.client.create_bucket(bucket_name="test")
        self.assertEqual(response_create["ResponseMetadata"]["HTTPStatusCode"], 200)

        response_head = self.client.head_bucket(bucket_name="test")
        self.assertEqual(response_head["ResponseMetadata"]["HTTPStatusCode"], 200)

        response_delete = self.client.delete_bucket(bucket_name="test")
        self.assertEqual(response_delete["ResponseMetadata"]["HTTPStatusCode"], 204)

        with self.assertRaises(botocore.exceptions.ClientError):
            self.client.head_bucket(bucket_name="test")
