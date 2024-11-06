provider "google" {
  project     = "azure-integration-405515"
}

variable "project_name" {}
variable "owner_email" {}

resource "google_project" "project" {
  name       = var.project_name
  project_id = var.project_name
  org_id     = "653492276671"
  billing_account = "0153E0-DDEFFA-D32EE6"
}

resource "google_project_iam_member" "owner" {
  project = google_project.project.project_id
  role    = "roles/owner"
  member  = "user:${var.owner_email}"
}
