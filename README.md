# DevOps Microservices Platform

This project is a complete, end-to-end **cloud-native microservices platform** built to showcase advanced **DevOps skills** using a modern CI/CD pipeline, infrastructure-as-code, configuration management, container orchestration, and automation tools.

> ⚠️ **Note:**  
> **Emphasis is on the automation workflow and not the functionality of the apps.**

> ✅ Ideal for portfolio, demo, or learning advanced DevOps workflows.

---

## 🚀 Project Overview

This platform consists of a 4-tier microservices application, containerized with Docker, orchestrated via Kubernetes (EKS), and deployed using Helm charts. It uses Terraform for infrastructure provisioning, Ansible for configuration management, and GitHub Actions for continuous integration and delivery.

---

## 🔧 Technologies Used

| Layer | Tools |
|------|-------|
| **Source Control & CI/CD** | Git, GitHub, GitHub Actions |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes (EKS) |
| **Infrastructure as Code** | Terraform |
| **Configuration Management** | Ansible |
| **Package Management** | Helm |
| **Cloud Provider** | AWS (S3, EKS, IAM, VPC, RDS/PostgreSQL) |
| **Automation Scripts** | Python |
| **Ingress & Exposure** | NGINX Ingress Controller |

---

## 🧱 Microservices Architecture

```
[user-service]      [product-service]
      |                   |
      +--------+----------+
               |
        [order-service]
               |
    [notification-service]
               |
         [PostgreSQL DB]
```

- All services are containerized and communicate over internal Kubernetes networking.
- Ingress routes external traffic to respective services via path-based routing.

---

## 🗂️ Project Structure

```
.
├── services/
│   ├── user_service/
│   ├── product_service/
│   ├── order_service/
│   ├── notification_service/
├── infrastructure/
│   └── terraform/      # AWS EKS, VPC, RDS setup
├── ansible/
│   └── playbooks/      # Install Docker, K8s tools
├── helm/
│   └── microservices/  # Helm chart for app deployment
├── scripts/
│   └── automation.py   # Python automation utilities
├── .github/
│   └── workflows/
│       └── python-app.yml  # GitHub Actions CI/CD pipeline
└── README.md
```

---

## 📦 Features

- 🛠️ **Infrastructure-as-Code**: Provision AWS resources with Terraform
- 📦 **Containerization**: Dockerize each microservice independently
- 🚀 **CI/CD**: Automatically build, test, push, and deploy services via GitHub Actions
- 🐳 **Orchestration**: Run all services in Kubernetes using Helm charts
- ⚙️ **Ansible Bootstrapping**: Setup of EC2 instances, kubeconfig, Docker engine
- 🔒 **Ingress**: NGINX ingress controller with path-based routing
- 🐍 **Python Automation**: Health checks, test scripts, and log processors

---

## 🛠️ Getting Started

### Prerequisites

- AWS account with permissions for EKS, IAM, EC2, S3, RDS
- Docker & kubectl installed locally
- GitHub repo connected
- GitHub Secrets configured:
  - `DOCKER_USERNAME`
  - `DOCKER_PASSWORD`
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION`
  - `AWS_ACCOUNT_ID`

---

### 1. Bootstrap S3 (for Terraform backend)

```bash
cd terraform/bootstrap
terraform init
terraform apply
```

Installs:

- S3 bucket

---

### 2. Provision Infrastructure (Terraform)

```bash
cd infrastructure/terraform
terraform init
terraform apply
```

Creates:

- VPC
- ECR
- Node Group
- EKS Cluster
- IAM roles
- RDS PostgreSQL

---

### 3. Build, Test & Push Microservices (CI/CD Pipeline)

#### **Automated via GitHub Actions:**

- **Static Code Analysis:** Lint each service with flake8.
- **Unit Tests:** Run pytest for each service.
- **Build & Smoke Test:** Build Docker images, run each container, and check `/health` endpoint.
- **Integration Test:** Start all containers in a shared Docker network, run end-to-end API tests between services.
- **Push:** Only if all tests pass, images are pushed to ECR or Docker Hub.

#### **Manual Example:**

```bash
docker build -t user-service ./services/user_service
docker run -d -p 5001:5001 user-service
curl http://localhost:5001/health
docker tag user-service:latest yourdockerhub/user-service:latest
docker push yourdockerhub/user-service:latest
```

---

### 4. Deploy with Helm

```bash
cd helm/microservices
helm upgrade --install microservices . -f values.yaml
```

---

## 🔁 CI/CD Pipeline Details

### 🛠️ Optional/Custom Flow

The CI/CD pipeline is designed for **flexibility** to support both default and custom workflows:
This enables you to run your desired workflow for desired services like dockerhub or AWS ECR, customs kubernetes server, AWS EKS or AWS ECS.

**Workflow:** python-app.yml

- **Trigger:** Push to `main`, PR, or manual dispatch
- **Stages:**
  1. **Static Code Analysis:** Lint with flake8
  2. **Unit Testing:** Run pytest
  3. **Build & Smoke Test:** Build Docker image, run container, check `/health`
  4. **Integration Test:** Start all containers, run cross-service API tests
  5. **Push:** Push image to registry only if all tests pass

---

### ⚡ How to Use

- **Edit `.github/workflows/python-app.yml`** to adjust the matrix, add `if:` conditions, or expose workflow inputs.
- **Trigger manually** from the GitHub Actions UI for custom runs.

---

## 📌 Future Enhancements

- [ ] Add Prometheus + Grafana for monitoring
- [ ] Add Jaeger for distributed tracing
- [ ] Add external-dns for Route53 integration
- [ ] Add TLS support via cert-manager
- [ ] Add more advanced test stages in pipeline

---

## 🙌 Credits

This lab was built to simulate a real-world DevOps workflow with cloud-native tools. It showcases advanced concepts in automation, scaling, and infrastructure orchestration.

---

## 📬 Contact

**Your Name**  
Email: [adexxy@live.com](mailto:adexxy@live.com)  
GitHub: [@Adexxy](https://github.com/adexxy)

---
