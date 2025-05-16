# DevOps Portfolio Lab

This lab demonstrates end-to-end DevOps practices for a microservices application. It covers:

- **Git & GitHub**: Version control, branching, PR workflows, CI via GitHub Actions
- **Terraform**: Provision AWS infrastructure (VPC, EKS, RDS)
- **AWS**: Hosted Kubernetes (EKS) and PostgreSQL (RDS)
- **Docker**: Containerize 4 microservices + database
- **Kubernetes & Helm**: Deploy with Helm charts and raw manifests
- **Ansible**: Bootstrap and configure Kubernetes nodes
- **CI/CD**: Automated pipelines with GitHub Actions (alternatively Jenkins or CircleCI)
- **Python Automation**: Scripts for backups and environment management

## Prerequisites

- AWS account with IAM permissions
- CLI tools: `aws`, `kubectl`, `helm`, `terraform`, `ansible`, `docker`
- GitHub repository

## Getting Started

1. **Clone Repo**

    ```bash
    git clone https://github.com/your-org/devops-portfolio-lab.git
    cd devops-portfolio-lab
    ```

2. **Terraform Infrastructure**

    ```bash
    cd terraform
    terraform init
    terraform apply -auto-approve
    ```

    This creates VPC, EKS cluster, and RDS instance.

3. **Ansible Bootstrap**

    ```bash
    cd ../ansible
    ansible-playbook -i inventory playbook.yml
    ```

4. **Build & Push Docker Images**

    ```bash
    cd services/*
    docker build -t <ECR_URI>/user-service:latest .
    docker push <ECR_URI>/user-service:latest
    # Repeat for each service and database image
    ```

5. **Deploy with Helm**

    ```bash
    cd ../helm-charts/microservices
    helm install microservices .
    ```

6. **CI/CD**
    - GitHub Actions runs on push/PR: builds images, runs tests, and deploys to EKS.

7. **Python Automation**

    ```bash
    python3 automation/backup.py --rds-endpoint <ENDPOINT> --output backups/
    ```
