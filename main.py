provider "aws" {
  region = var.aws_region
  
  # Use custom endpoints for LocalStack if enabled
  dynamic "endpoints" {
    for_each = var.use_localstack ? [1] : []
    content {
      s3 = var.s3_endpoint
    }
  }
  
  # Skip credential validation and metadata API check for LocalStack
  skip_credentials_validation = var.use_localstack
  skip_metadata_api_check     = var.use_localstack
  skip_requesting_account_id  = var.use_localstack
  
  # LocalStack specific configurations
  s3_use_path_style = var.use_localstack
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = var.bucket_name

  lifecycle {
    prevent_destroy = false
  }

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
    Managed     = "terraform"
  }
}

resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "block" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "s3_bucket_id" {
  value       = aws_s3_bucket.terraform_state.id
  description = "The ID of the S3 bucket"
}

output "s3_bucket_arn" {
  value       = aws_s3_bucket.terraform_state.arn
  description = "The ARN of the S3 bucket"
}
