data "terraform_remote_state" "shared" {
  backend = "s3"
  config = {
    bucket = "runtime-revolution-dev-env"
    key    = "shared/terraform.tfstate"
  }
}
