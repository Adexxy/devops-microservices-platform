# outputs.tf
output "ecr_repos" {
  value = {
    for name, repo in aws_ecr_repository.services : name => repo.repository_url
  }
}