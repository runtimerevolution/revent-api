from django.test import TestCase

from integrations.aws.s3 import Client


class S3BucketTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()

    def test_create(self):
        response_create = self.client.create_bucket(bucket_name="test")
        self.assertEqual(response_create["ResponseMetadata"]["HTTPStatusCode"], 200)

    def test_bucket_exists(self):
        self.client.create_bucket(bucket_name="test-existence")
        exists = self.client.check_bucket_existence(bucket_name="test-existence")
        not_exists = self.client.check_bucket_existence(bucket_name="not_existence")

        self.assertEqual(exists, True)
        self.assertEqual(not_exists, False)

    def test_bucket_delete(self):
        self.client.create_bucket(bucket_name="test-delete")
        response_delete = self.client.delete_bucket(bucket_name="test-delete")
        bucket_exists = self.client.check_bucket_existence(bucket_name="test-delete")

        self.assertEqual(response_delete["ResponseMetadata"]["HTTPStatusCode"], 204)
        self.assertEqual(bucket_exists, False)

    def tearDown(self) -> None:
        if self.client.check_bucket_existence("test"):
            self.client.delete_bucket(bucket_name="test")
        if self.client.check_bucket_existence("test-existence"):
            self.client.delete_bucket(bucket_name="test-existence")
        return super().tearDown()
