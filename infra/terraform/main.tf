terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {}
variable "region"    { default = "us-central1" }

# -------------------------------------------------
# Service Account (used by all Cloud Functions)
# -------------------------------------------------
resource "google_service_account" "capstone_sa" {
  account_id   = "capstone-sa"
  display_name = "Capstone Service Account"
}

# Grant least‑privilege roles (add/remove as needed)
resource "google_project_iam_member" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.capstone_sa.email}"
}
resource "google_project_iam_member" "bigquery_admin" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.capstone_sa.email}"
}
resource "google_project_iam_member" "pubsub_admin" {
  project = var.project_id
  role    = "roles/pubsub.admin"
  member  = "serviceAccount:${google_service_account.capstone_sa.email}"
}
resource "google_project_iam_member" "cloudfunctions_admin" {
  project = var.project_id
  role    = "roles/cloudfunctions.admin"
  member  = "serviceAccount:${google_service_account.capstone_sa.email}"
}
resource "google_project_iam_member" "scheduler_admin" {
  project = var.project_id
  role    = "roles/cloudscheduler.admin"
  member  = "serviceAccount:${google_service_account.capstone_sa.email}"
}
resource "google_project_iam_member" "secretmanager_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.capstone_sa.email}"
}

# -------------------------------------------------
# Cloud Storage bucket for raw JSON
# -------------------------------------------------
resource "google_storage_bucket" "raw_bucket" {
  name          = "${var.project_id}-mh-raw"
  location      = var.region
  force_destroy = true
  uniform_bucket_level_access = true
}

# -------------------------------------------------
# BigQuery dataset
# -------------------------------------------------
resource "google_bigquery_dataset" "mh_dataset" {
  dataset_id = "mental_health"
  location   = var.region
  delete_contents_on_destroy = true
}

# -------------------------------------------------
# Pub/Sub topic for alerts
# -------------------------------------------------
resource "google_pubsub_topic" "mh_alerts" {
  name = "mh_alerts"
}

# -------------------------------------------------
# Cloud Scheduler job (runs collector daily at 00:30 UTC)
# -------------------------------------------------
resource "google_cloud_scheduler_job" "collector_job" {
  name             = "mh-collector"
  description      = "Runs the Twitter & Reddit collector Cloud Function daily"
  schedule         = "30 0 * * *"
  time_zone        = "Etc/UTC"
  attempt_deadline = "320s"

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions_function.collector.https_trigger_url
    oidc_token {
      service_account_email = google_service_account.capstone_sa.email
    }
  }
}

# -------------------------------------------------
# Cloud Functions (Docker container)
# -------------------------------------------------
resource "google_cloudfunctions2_function" "collector" {
  name        = "collect_posts"
  location    = var.region
  build_config {
    runtime = "python311"
    entry_point = "collect"
    source {
      # The Docker image built by CI
      docker_repository = "us-central1-docker.pkg.dev/${var.project_id}/capstone-repo/mh-monitor"
      docker_image      = "latest"
    }
    environment_variables = {
      RAW_BUCKET = google_storage_bucket.raw_bucket.name
      TWITTER_BEARER = "PLACEHOLDER"   # set via Secret Manager later
    }
  }
  service_config {
    max_instance_count = 2
    available_memory   = "256Mi"
    timeout_seconds    = 540
    service_account_email = google_service_account.capstone_sa.email
  }
}

/* Repeat the above block for the other functions:
   - clean_and_load
   - score_posts
   - compute_alert
   - send_alert
   Change `entry_point` and `environment_variables` accordingly.
*/

output "collector_url" {
  value = google_cloudfunctions2_function.collector.service_config[0].uri
}
