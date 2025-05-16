**Project Structure**

```
devops-portfolio-lab/
├── README.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── modules/
│       ├── vpc/
│       ├── eks/
│       └── rds/
├── ansible/
│   └── playbook.yml
├── helm-charts/
│   └── microservices/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           └── ingress.yaml
├── k8s-manifests/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   └── secrets.yaml
├── services/
│   ├── user-service/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── product-service/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── order-service/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── notification-service/
│       ├── app.py
│       ├── requirements.txt
│       └── Dockerfile
├── database/
│   ├── init.sql
│   └── Dockerfile
└── automation/
    └── backup.py
```

---

## README.md

````markdown
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

---

## Code Samples

### Terraform: `terraform/main.tf`
```hcl
provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "./modules/vpc"
  cidr_block = var.vpc_cidr
}

module "eks" {
  source          = "./modules/eks"
  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version
  subnets         = module.vpc.public_subnets
}

module "rds" {
  source           = "./modules/rds"
  db_name          = var.db_name
  db_username      = var.db_username
  db_password      = var.db_password
  vpc_security_group_ids = [module.vpc.default_sg]
  subnet_ids       = module.vpc.private_subnets
}
````

### Ansible: `ansible/playbook.yml`

```yaml
- name: Bootstrap EKS nodes
  hosts: eks_nodes
  become: yes
  tasks:
    - name: Install Docker
      apt:
        name: docker.io
        state: present
    - name: Add Kubernetes repo
      apt_repository:
        repo: deb http://apt.kubernetes.io/ kubernetes-xenial main
    - name: Install kubectl
      apt:
        name: kubectl
        state: present
    - name: Join Node to Cluster
      shell: kubeadm join {{ kubeadm_join_cmd }}
```

### Helm Chart: `helm-charts/microservices/values.yaml`

```yaml
replicaCount: 2
image:
  repository: <ECR_URI>/microservices
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 80
ingress:
  enabled: true
  host: example.com
```

### Kubernetes Namespace: `k8s-manifests/namespace.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: microservices
```

### Service Dockerfile: `services/user-service/Dockerfile`

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

### Example Microservice: `services/user-service/app.py`

```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/users')
def list_users():
    return jsonify([{'id': 1, 'name': 'Alice'}])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

### GitHub Actions CI: `.github/workflows/ci.yml`

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Build and Test Services
        run: |
          for svc in services/*; do
            cd "$svc"
            pip install -r requirements.txt
            # Add unit tests here
            cd -
          done
      - name: Build Docker Images
        run: |
          for svc in services/*; do
            cd "$svc"
            docker build -t ${{ secrets.ECR_URI }}/${{ basename $svc }}:latest .
            docker push ${{ secrets.ECR_URI }}/${{ basename $svc }}:latest
            cd -
          done
      - name: Deploy Helm Chart
        run: |
          helm upgrade --install microservices helm-charts/microservices
```

### Python Automation: `automation/backup.py`

```python
import argparse
import boto3
import datetime
import os

def backup_rds(endpoint, output_dir):
    client = boto3.client('rds')
    snapshot_id = f"backup-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    client.create_db_snapshot(
        DBSnapshotIdentifier=snapshot_id,
        DBInstanceIdentifier=endpoint
    )
    print(f"Triggered snapshot: {snapshot_id}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rds-endpoint', required=True)
    parser.add_argument('--output', default='backups/')
    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)
    backup_rds(args.rds_endpoint, args.output)
```



**Microservices Code Generation**

Below are the full code listings for each microservice (product, order, notification) and the database initialization. Each service has its `app.py`, `requirements.txt`, and `Dockerfile`.

---

### 1. Product Service (`services/product-service`)

```python
# services/product-service/app.py
from flask import Flask, jsonify, request
app = Flask(__name__)

# In-memory product store
products = [
    {'id': 1, 'name': 'Widget', 'price': 9.99},
    {'id': 2, 'name': 'Gadget', 'price': 12.49}
]

@app.route('/products', methods=['GET'])
def list_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    p = next((p for p in products if p['id'] == product_id), None)
    if not p:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(p)

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_id = max(p['id'] for p in products) + 1
    product = {'id': new_id, 'name': data['name'], 'price': data['price']}
    products.append(product)
    return jsonify(product), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

```text
# services/product-service/requirements.txt
Flask==2.1.2
```

```dockerfile
# services/product-service/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

---

### 2. Order Service (`services/order-service`)

```python
# services/order-service/app.py
from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

ORDERS = []
PRODUCT_SERVICE_URL = "http://product-service.microservices.svc.cluster.local"

@app.route('/orders', methods=['GET'])
def list_orders():
    return jsonify(ORDERS)

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    # validate product exists
    resp = requests.get(f"{PRODUCT_SERVICE_URL}/products/{data['product_id']}")
    if resp.status_code != 200:
        return jsonify({'error': 'Product not found'}), 400
    order = {
        'id': len(ORDERS) + 1,
        'product_id': data['product_id'],
        'quantity': data.get('quantity', 1)
    }
    ORDERS.append(order)
    return jsonify(order), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

```text
# services/order-service/requirements.txt
Flask==2.1.2
requests==2.28.1
```

```dockerfile
# services/order-service/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

---

### 3. Notification Service (`services/notification-service`)

```python
# services/notification-service/app.py
from flask import Flask, request
import requests
app = Flask(__name__)

ORDER_SERVICE_URL = "http://order-service.microservices.svc.cluster.local"

@app.route('/notify', methods=['POST'])
def send_notification():
    data = request.get_json()
    order_id = data.get('order_id')
    # simulate fetching order details
    resp = requests.get(f"{ORDER_SERVICE_URL}/orders")
    if resp.status_code != 200:
        return {'status': 'failed'}, 500
    # In real-world, push to email/SMS queue
    print(f"Notification: Order {{order_id}} processed.")
    return {'status': 'sent'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

```text
# services/notification-service/requirements.txt
Flask==2.1.2
requests==2.28.1
```

```dockerfile
# services/notification-service/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

---

### 4. Database Initialization (`database`)

```sql
-- database/init.sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100)
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  price NUMERIC(10,2)
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  product_id INTEGER REFERENCES products(id),
  quantity INTEGER
);
```

```dockerfile
# database/Dockerfile
FROM postgres:13-alpine
COPY init.sql /docker-entrypoint-initdb.d/init.sql
```

---

With these codebases in place, you can build, push, and deploy each Docker image as part of your CI/CD pipeline. Let me know if you want automated tests or further environment configuration!




**Microservices Enhancements: Health‑Checks, Unit Tests & User‑Service Update**

This canvas adds:

1. **Health‑check endpoints** for each service
2. **Unit tests** (using `pytest`) for all four microservices
3. **Enhanced User Service** with full CRUD operations

---

## 1. User Service (Enhanced)

**File: `services/user-service/app.py`**

```python
from flask import Flask, jsonify, request, abort
app = Flask(__name__)

# In-memory store
users = [
    {'id': 1, 'name': 'Alice'},
    {'id': 2, 'name': 'Bob'}
]

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/users', methods=['GET'])
def list_users():
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    u = next((u for u in users if u['id'] == user_id), None)
    if not u:
        abort(404)
    return jsonify(u)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400)
    new_id = max(u['id'] for u in users) + 1
    user = {'id': new_id, 'name': data['name']}
    users.append(user)
    return jsonify(user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    u = next((u for u in users if u['id'] == user_id), None)
    if not u:
        abort(404)
    if not data or 'name' not in data:
        abort(400)
    u['name'] = data['name']
    return jsonify(u)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

**Add** `health()` in other services similarly (`/health` returning `{'status':'ok'}`).

---

## 2. Health‑Check Endpoints

Add this snippet to each `app.py` above the main routes:

```python
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200
```

---

## 3. Unit Tests (pytest)

Create a `tests/` directory at repo root. For each service, add tests:

### 3.1 User Service Tests (`tests/test_user_service.py`)

```python
import pytest
from services.user_service.app import app as user_app

test_client = user_app.test_client()

def test_health():
    resp = test_client.get('/health')
    assert resp.status_code == 200
    assert resp.get_json() == {'status': 'ok'}

def test_create_and_get_user():
    # Create
    resp = test_client.post('/users', json={'name': 'Charlie'})
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'id' in data and data['name'] == 'Charlie'
    uid = data['id']
    # Retrieve
    resp2 = test_client.get(f'/users/{uid}')
    assert resp2.status_code == 200
    assert resp2.get_json()['name'] == 'Charlie'

def test_update_user():
    # Create dummy
    resp = test_client.post('/users', json={'name': 'Dave'})
    uid = resp.get_json()['id']
    # Update
    resp2 = test_client.put(f'/users/{uid}', json={'name': 'David'})
    assert resp2.status_code == 200
    assert resp2.get_json()['name'] == 'David'

def test_delete_user():
    resp = test_client.post('/users', json={'name': 'Eve'})
    uid = resp.get_json()['id']
    resp2 = test_client.delete(f'/users/{uid}')
    assert resp2.status_code == 204
    # Verify gone
    resp3 = test_client.get(f'/users/{uid}')
    assert resp3.status_code == 404
```

### 3.2 Product Service Tests (`tests/test_product_service.py`)

```python
import pytest
from services.product_service.app import app as product_app

test_client = product_app.test_client()

def test_health():
    resp = test_client.get('/health')
    assert resp.status_code == 200

def test_list_and_get():
    resp = test_client.get('/products')
    assert resp.status_code == 200
    products = resp.get_json()
    assert isinstance(products, list)
    pid = products[0]['id']
    resp2 = test_client.get(f'/products/{pid}')
    assert resp2.status_code == 200

def test_create_product():
    resp = test_client.post('/products', json={'name':'Thing','price':5.0})
    assert resp.status_code == 201
    assert 'id' in resp.get_json()
```

### 3.3 Order Service Tests (`tests/test_order_service.py`)

```python
import pytest
from unittest.mock import patch
from services.order_service.app import app as order_app

client = order_app.test_client()

@patch('services.order_service.app.requests.get')
def test_create_order_success(mock_get):
    mock_get.return_value.status_code = 200
    data = {'product_id': 1, 'quantity':2}
    resp = client.post('/orders', json=data)
    assert resp.status_code == 201
    assert resp.get_json()['product_id'] == 1

@patch('services.order_service.app.requests.get')
def test_create_order_fail(mock_get):
    mock_get.return_value.status_code = 404
    resp = client.post('/orders', json={'product_id':999})
    assert resp.status_code == 400
```

### 3.4 Notification Service Tests (`tests/test_notification_service.py`)

```python
import pytest
from unittest.mock import patch
from services.notification_service.app import app as notif_app

client = notif_app.test_client()

def test_health():
    resp = client.get('/health')
    assert resp.status_code == 200

@patch('services.notification_service.app.requests.get')
def test_notify(mock_get):
    mock_get.return_value.status_code = 200
    resp = client.post('/notify', json={'order_id':1})
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'sent'
```

---

Install `pytest` in each `requirements.txt` (or a shared `requirements-dev.txt`):

```
pytest==7.1.2
```

Run tests with:

```bash
pytest tests/
```

---

These additions complete health monitoring, test coverage, and an enhanced user‑service CRUD example. Let me know if you’d like CI integration for these tests or further end‑to‑end scenarios!
