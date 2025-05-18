# DevOps Microservices Platform

This project is a complete, end-to-end **cloud-native microservices platform** built to showcase advanced **DevOps skills** using a modern CI/CD pipeline, infrastructure-as-code, configuration management, container orchestration, and automation tools.

> ✅ Ideal for portfolio, demo, or learning advanced DevOps workflows.

---

## 🚀 Project Overview

This platform consists of a 4-tier microservices application, containerized with Docker, orchestrated via Kubernetes (EKS), and deployed using Helm charts. It uses Terraform for infrastructure provisioning, Ansible for configuration management, and GitHub Actions for continuous integration and delivery.

---

## 🔧 Technologies Used

| Layer | Tools |
|------|-------|
| **Source Control & CI/CD** | Git, GitHub, GitHub Actions, Jenkins (optional), CircleCI (optional) |
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

\[ user-service ]       \[ product-service ]
\|                       |
\|                       |
\[ order-service ]     \[ notification-service ]
|
\[ PostgreSQL DB ]

```

- All services are containerized and communicate over internal Kubernetes networking.
- Ingress routes external traffic to respective services via path-based routing.

---

## 🗂️ Project Structure

```

.
├── services/
│   ├── user\_service/
│   ├── product\_service/
│   ├── order\_service/
│   ├── notification\_service/
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
│       └── deploy.yml  # GitHub Actions CI/CD pipeline
└── README.md

````

---

## 📦 Features

- 🛠️ **Infrastructure-as-Code**: Provision AWS resources with Terraform
- 📦 **Containerization**: Dockerize each microservice independently
- 🚀 **CI/CD**: Automatically build, push, and deploy services via GitHub Actions
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
  - `KUBECONFIG_SECRET` (base64-encoded or plaintext kubeconfig)

---

### 1. Provision Infrastructure (Terraform)

```bash
cd infrastructure/terraform
terraform init
terraform apply
````

Creates:

* VPC
* EKS Cluster
* IAM roles
* RDS PostgreSQL (optional)

---

### 2. Bootstrap EC2 Nodes (Ansible)

```bash
cd ansible/playbooks
ansible-playbook setup-k8s-nodes.yml -i inventory
```

Installs:

* Docker
* kubelet, kubeadm
* Helm, kubectl
* Configures node joining

---

### 3. Build & Push Microservices (GitHub Actions or manually)

Manual:

```bash
docker build -t user-service ./services/user_service
docker tag user-service:latest yourdockerhub/user-service:latest
docker push yourdockerhub/user-service:latest
```

Or let GitHub Actions do it automatically on `git push`.

---

### 4. Deploy with Helm

```bash
cd helm/microservices
helm upgrade --install microservices . -f values.yaml
```

---

### 5. Access the Application

Ensure NGINX Ingress Controller is installed:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/aws/deploy.yaml
```

Then access services via:

```
http://<external-ip>/user
http://<external-ip>/product
http://<external-ip>/order
http://<external-ip>/notification
```

Use `kubectl get ingress` to fetch the external IP or hostname.

---

## 🔁 CI/CD Pipeline

GitHub Actions Workflow (`.github/workflows/deploy.yml`):

* Trigger: Push to `main`
* Steps:

  * Build and push Docker images
  * Deploy via Helm
  * Optionally notify via Slack/Webhooks

---

## 📌 Future Enhancements

* [ ] Add Prometheus + Grafana for monitoring
* [ ] Add Jaeger for distributed tracing
* [ ] Add external-dns for Route53 integration
* [ ] Add TLS support via cert-manager
* [ ] Add unit/integration test stages in pipeline

---

## 🙌 Credits

This lab was built to simulate a real-world DevOps workflow with cloud-native tools. It showcases advanced concepts in automation, scaling, and infrastructure orchestration.

---

## 📄 License



---

## 📬 Contact

**Your Name**
Email: [you@example.com](mailto:adexxy@live.com)
GitHub: [@your-github-handle](https://github.com/your-github-handle)

```

---


