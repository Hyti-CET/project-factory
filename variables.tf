variable "billing_project_id" {
  description = "The existing project ID where billing is linked"
  type        = string
}

variable "project_name" {
  description = "The name of the new project"
  type        = string
}

variable "project_id" {
  description = "The unique ID for the new project"
  type        = string
}

variable "billing_account_id" {
  description = "The billing account ID to associate with the new project"
  type        = string
}

variable "owner_email" {
  description = "The email of the service account owner for IAM roles"
  type        = string
}

variable "vpc_name" {
  description = "The name of the VPC to create"
  type        = string
  default     = "my-vpc"
}

variable "region" {
  description = "The region to deploy resources"
  type        = string
  default     = "us-central1"
}
