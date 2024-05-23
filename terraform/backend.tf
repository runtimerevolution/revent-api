terraform {
  backend "s3" {
    bucket = "runtime-revolution-dev-env"
    key    = "revent/terraform.tfstate"
  }
}
