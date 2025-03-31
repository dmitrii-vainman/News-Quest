provider "aws" {
  region = var.aws_region
}

resource "tls_private_key" "my_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "my_key_file" {
  file_permission = 0600
  content         = tls_private_key.my_key.private_key_pem
  filename        = "${path.module}/news_key.pem"
}



resource "aws_key_pair" "my_aws_key" {
  key_name   = "news_key"
  public_key = tls_private_key.my_key.public_key_openssh

}

resource "aws_security_group" "newsquest_sg" {
  name        = "newsquest_security_group"
  description = "Security group for News-Quest"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Update to restrict access
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Open FastAPI endpoint
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Open for HTTP traffic
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "newsquest_backend" {
  ami                    = var.ec2_ami
  instance_type          = var.instance_type
  key_name               = aws_key_pair.my_aws_key.key_name
  security_groups        = [aws_security_group.newsquest_sg.name]
  associate_public_ip_address = true

  tags = {
    Name = "NewsQuest-Backend"
  }
}

output "ec2_public_ip" {
  value = aws_instance.newsquest_backend.public_ip
}

output "ssh_command" {
  value = "ssh -i news_key.pem ubuntu@${aws_instance.newsquest_backend.public_ip}"
}

resource "aws_s3_bucket" "newsquest_frontend" {
  bucket = var.s3_bucket_name
}


resource "aws_s3_bucket_public_access_block" "site" {
  bucket = var.s3_bucket_name

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}


resource "aws_s3_bucket_website_configuration" "site" {
  bucket = var.s3_bucket_name

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_ownership_controls" "site" {
  bucket = var.s3_bucket_name
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
  depends_on = [aws_s3_bucket.newsquest_frontend]
}

resource "aws_s3_bucket_acl" "site" {
  bucket = var.s3_bucket_name

  acl = "public-read"
  depends_on = [
    aws_s3_bucket_ownership_controls.site,
    aws_s3_bucket_public_access_block.site
  ]
}

resource "aws_s3_bucket_policy" "site" {
  bucket = var.s3_bucket_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource = [
          aws_s3_bucket.newsquest_frontend.arn,
          "${aws_s3_bucket.newsquest_frontend.arn}/*",
        ]
      },
    ]
  })

  depends_on = [
    aws_s3_bucket_public_access_block.site
  ]
}

resource "aws_s3_object" "index" {
  bucket       = var.s3_bucket_name
  key          = "index.html"
  source       = "../client/dist/index.html" # Update the path where your index.html is stored
  content_type = "text/html"
  acl          = "public-read"
  depends_on = [
    aws_s3_bucket_ownership_controls.site,
    aws_s3_bucket_public_access_block.site
  ]
}

resource "aws_s3_object" "error" {
  bucket       = var.s3_bucket_name
  key          = "error.html"
  source       = "../client/dist/error.html" # Update the path where your error.html is stored
  content_type = "text/html"
  acl          = "public-read"
  depends_on = [
    aws_s3_bucket_ownership_controls.site,
    aws_s3_bucket_public_access_block.site
  ]
}