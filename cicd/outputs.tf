/******************************************
  Project
*******************************************/

output "cicd_project_id" {
  description = "Project where the cid pipeline is established."
  value       = google_project.cicd.project_id
}

/******************************************
  Repository
*******************************************/
output "cicd_repository_url" {
  description = "source code repository url"
  value       = google_sourcerepo_repository.configs.url
}


/******************************************
  GCS Terraform State Bucket
*******************************************/

output "gcs_bucket_tfstate" {
  description = "Bucket used for storing terraform state the project."
  value       = google_storage_bucket.project_terraform_state.name
}
