variable "aws_region" {
  description = "The AWS region to deploy the EKS cluster"
  type        = string
}

variable "cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
}

variable "node_group_name" {
  description = "The name of the EKS node group"
  type        = string
}

variable "namespace" {
  description = "The namespace to deploy the URL shortener service"
  type        = string
}

variable "image_tag" {
  description = "value of the image tag"
  type        = string
}