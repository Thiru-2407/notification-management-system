# Notification Management System

An enterprise-ready, three-version Notification Management System built with Python Flask, SQLite, Docker, Kubernetes, and Jenkins CI/CD.

## Architecture & Versions

| Feature / Capability | Version 1 (v1) | Version 2 (v2) | Version 3 (v3) |
| :--- | :--- | :--- | :--- |
| **Storage Architecture** | In-Memory Data Structure | Persistent SQLite DB (`notifications_v2.db`) | Indexed SQLite DB with Migration Support (`notifications_v3.db`) |
| **Input Validation** | Basic Presence Validation | Length & Boundary Validation (Title 3-100, Message 5-500) | Strict Validation, Type Enforcement & Priority Checks |
| **Alert Priorities** | Standard Alerts | Standard Alerts | 4 Severity Levels: `INFO`, `WARNING`, `CRITICAL`, `SUCCESS` |
| **Timestamping** | Server Local Timestamp | Formatted ISO / Display Timestamps | High-Precision UTC Timestamps & Live Filters |
| **Error Handling** | Basic HTTP 400 & 404 | Field-Specific Validation Feedback | Custom Handlers (400, 404, 500) & Flash Notifications |
| **User Interface** | Basic Minimalist HTML/CSS | Split-Panel Layout with Modern Cards | Polished Glassmorphic Dashboard with Live Metrics & Badges |
| **REST API** | Full CRUD JSON Endpoints | Full CRUD + Persistence | Full CRUD + Priority Filtering (`?priority=...`) |
| **Kubernetes Service Port** | `8081` (`notification-v1-service`) | `8082` (`notification-v2-service`) | `8083` (`notification-v3-service`) |

---

## Local Development & Setup

### Prerequisites
- Python 3.11+
- Git 2.40+
- Docker Engine & Docker Hub Account
- Kubernetes Cluster (`kubectl` configured)

### Running Locally
```powershell
# Install dependencies
pip install -r requirements.txt

# Run Version 1
python app/app.py

# Run Automated Tests
pytest tests/ -v
```

---

## Docker Containerization

### Building Images
```bash
docker build -t thiru247/notification-system:v1 .
docker build -t thiru247/notification-system:v2 -f versions/v2/Dockerfile versions/v2/
docker build -t thiru247/notification-system:v3 -f versions/v3/Dockerfile versions/v3/
```

### Running Containers Locally
```bash
docker run -d -p 8081:8080 --name notif-v1 thiru247/notification-system:v1
docker run -d -p 8082:8080 --name notif-v2 thiru247/notification-system:v2
docker run -d -p 8083:8080 --name notif-v3 thiru247/notification-system:v3
```

---

## Kubernetes Deployment

Deploy all three versions to Kubernetes:
```bash
kubectl apply -f kubernetes/v1-deployment.yaml
kubectl apply -f kubernetes/v1-service.yaml
kubectl apply -f kubernetes/v2-deployment.yaml
kubectl apply -f kubernetes/v2-service.yaml
kubectl apply -f kubernetes/v3-deployment.yaml
kubectl apply -f kubernetes/v3-service.yaml
```

Access endpoints:
- **v1:** `http://localhost:8081`
- **v2:** `http://localhost:8082`
- **v3:** `http://localhost:8083`

---

## Jenkins CI/CD Pipeline

The declarative `Jenkinsfile` automates:
1. Multi-branch / parameterized checkout (`APP_VERSION` = v1, v2, v3)
2. Automated pytest execution
3. Docker image build and semantic tagging
4. Secure Docker Hub credential authentication
5. Automated container image publishing to Docker Hub
