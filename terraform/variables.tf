variable "aws_region" {
  default = "eu-central-1"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_name" {
  description = "key"
  default = "universal2025"
}

variable "s3_bucket_name" {
  description = "newsquestbucket"
  type        = string
  default     = "newsquest-bucket"  # Set a valid default value
}

variable "ec2_ami" {
  description = "ubuntu 22.04"
  default     = "ami-04a5bacc58328233d" 
}

variable "ec2_user" {
  description = "EC2 newsq"
  default     = "ubuntu newsq"
}

variable "site_domain" {
  default     = "news-quest-domain"
  description = "project news-quest"
}