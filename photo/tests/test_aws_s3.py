from random import randint
import io

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from commons.aws_s3 import awsS3

BINARY_CONTENT = b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01"


class AWSS3Tests(TestCase):
    def test_empty_bucket(self):
        s3_client = awsS3()
        s3_client.create_bucket(f"{randint(0, 10000)}")
        assert s3_client.list_objs().get("Contents") == None

    def test_upload_file_object(self):
        s3_client = awsS3()
        f = io.BytesIO(BINARY_CONTENT)
        _file = SimpleUploadedFile("text.txt", f.read())
        contents = s3_client.list_objs().get("Contents")
        if contents == None:
            len_before = 0
        else:
            len_before = len(contents)

        s3_client.upload_file_obj(_file, f"test{randint(0, 10000)}.txt")

        assert (len_before + 1) == len(s3_client.list_objs().get("Contents"))

    def test_get_file_object(self):
        s3_client = awsS3()
        f = io.BytesIO(BINARY_CONTENT)
        file_name = f"test{randint(0, 10000)}.txt"
        _file = SimpleUploadedFile(file_name, f.read())
        f.seek(0)  # We need to reset the 'read pointer' after being read

        len_before = len(s3_client.list_objs().get("Contents"))

        s3_client.upload_file_obj(_file, _file.name)
        obj = s3_client.get_file_obj(file_name)

        assert (len_before + 1) == len(s3_client.list_objs().get("Contents"))
        assert obj.get("Body").read() == f.read()
