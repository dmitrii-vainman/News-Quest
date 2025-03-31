output "backend_public_ip" {
  value = aws_instance.newsquest_backend.public_ip
}

output "s3_bucket_name" {
  value = aws_s3_bucket.newsquest_frontend.bucket
}
