from storages.backends.s3 import S3Storage


class PublicMediaStorage(S3Storage):
    location = "http://127.0.0.1:4566/media"
    default_acl = "public-read"
    file_overwrite = False
