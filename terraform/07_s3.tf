resource "aws_s3_bucket" "revent_env_bucket" {
  bucket = var.s3_env_bucket
}

resource "aws_s3_object" "revent_api_env" {
  bucket = aws_s3_bucket.revent_env_bucket.bucket
  key    = ".env/api.env"
  source = "../.env/terraform/dev/api.env"
}

resource "aws_s3_object" "revent_app_env" {
  bucket = aws_s3_bucket.revent_env_bucket.bucket
  key    = ".env/app.env"
  source = "../.env/terraform/dev/app.env"
}

resource "aws_s3_object" "revent_nginx_env" {
  bucket = aws_s3_bucket.revent_env_bucket.bucket
  key    = ".env/nginx.env"
  source = "../.env/terraform/dev/nginx.env"
}

resource "aws_s3_bucket" "revent_storage_bucket" {
  bucket = var.s3_storage_bucket
}

resource "aws_s3_bucket_ownership_controls" "revent_storage_bucket" {
  bucket = aws_s3_bucket.revent_storage_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "revent_storage_bucket" {
  bucket = aws_s3_bucket.revent_storage_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "revent_storage_bucket" {
  bucket = aws_s3_bucket.revent_storage_bucket.id
  acl    = "public-read"

  depends_on = [
    aws_s3_bucket_ownership_controls.revent_storage_bucket,
    aws_s3_bucket_public_access_block.revent_storage_bucket,
  ]
}

data "aws_iam_policy_document" "revent_storage_bucket" {
  policy_id = "revent-storage-bucket"

  statement {
    actions = [
      "s3:GetObject"
    ]
    effect = "Allow"
    resources = [
      "${aws_s3_bucket.revent_storage_bucket.arn}/*"
    ]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    sid = "S3IconsBucketPublicAccess"
  }
}

resource "aws_s3_bucket_policy" "revent_storage_bucket" {
  bucket = aws_s3_bucket.revent_storage_bucket.id
  policy = data.aws_iam_policy_document.revent_storage_bucket.json
}
