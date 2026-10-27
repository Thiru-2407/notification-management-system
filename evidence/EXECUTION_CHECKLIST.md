# DevOps Execution Checklist: Notification Management System

**Project Name:** Notification Management System  
**Engineer:** Senior DevOps Engineer  
**Workspace:** `C:\Users\thiru\.gemini\antigravity\scratch\notification-management-system`  
**Date:** October 27, 2026  

---

## Stage 1: Environment & Tool Inspection
- [x] Inspect OS, User, and System Architecture (Windows 11, victus-tk\thiru)
- [x] Check VS Code installation & CLI (VS Code 1.143.1 x64)
- [x] Check Git version and global user identity (Git 2.55.0.windows.5, Thiru-2407 / thirukumarankarthi@gmail.com)
- [x] Check Python and Pip versions (Python 3.14.4, Pip 26.0.1)
- [x] Verify Python libraries (Flask 3.1.3, pytest 9.1.1, playwright 1.64.0, requests 2.34.2)
- [x] Discover Docker Hub user identity from local configuration (`thiru247`)
- [x] Initialize and verify Docker Engine / daemon (Docker 29.1.3 active in WSL2, exposed via TCP)
- [x] Inspect Kubernetes environment (k3s v1.36.5 cluster active, kubectl configured on Windows)
- [x] Inspect Jenkins availability (Jenkins LTS active in Docker container on port 8080)
- [x] Save initial environment output to `evidence/01_environment/tool_versions.txt`
- [x] Capture tool versions visual evidence / screenshot `evidence/01_environment/tool_versions.png`

---

## Stage 2: Application Development & Local Verification
### Version 1 (v1)
- [x] Create v1 source code (`app.py`, basic in-memory CRUD, simple HTML UI)
- [x] Create v1 HTML templates (`templates/index.html`) & CSS (`static/style.css`)
- [x] Create `requirements.txt` for v1
- [x] Create automated tests (`tests/test_app.py`) for v1 (7 tests covering CRUD, empty state, invalid input, 404, form)
- [x] Run automated tests for v1 and record output in `evidence/04_tests/v1_test_results.txt`
- [x] Run v1 web application locally and verify CRUD
- [x] Capture visual evidence: `evidence/02_application/v1_homepage.png`, `evidence/04_tests/v1_test_results.png`

### Version 2 (v2)
- [x] Create v2 source code with improved UI, input validation, and SQLite persistent storage (`versions/v2/`)
- [x] Create v2 HTML templates & styling
- [x] Create automated tests for v2 (6 tests covering persistence, boundaries, form submission)
- [x] Run automated tests for v2 and record output in `evidence/04_tests/v2_test_results.txt`
- [x] Run v2 web application locally and verify CRUD & persistence
- [x] Capture visual evidence: `evidence/02_application/v2_homepage.png`, `evidence/04_tests/v2_test_results.png`

### Version 3 (v3)
- [x] Create v3 source code with advanced error handling, formatted timestamps, strict validation, status badges, and polished UI (`versions/v3/`)
- [x] Create v3 HTML templates, modern styling, and flash alerts
- [x] Create automated tests for v3 (6 tests covering priorities, metrics, edge cases, error handlers)
- [x] Run automated tests for v3 and record output in `evidence/04_tests/v3_test_results.txt`
- [x] Run v3 web application locally and verify CRUD & polished UI
- [x] Capture visual evidence: `evidence/02_application/v3_homepage.png`, `evidence/04_tests/v3_test_results.png`

---

## Stage 3: GitHub Version Control
- [x] Initialize Git repository in the project folder
- [x] Configure `.gitignore`
- [x] Commit and branch `v1` (Commit `d813c45`)
- [x] Commit and branch `v2` (Commit `5628b3d`)
- [x] Commit and branch `v3` (Commit `1dfdac6`)
- [x] Merge / align `main` branch (Commit `d95ae22`)
- [x] Save git status, branch list, and commit log to `evidence/03_github/`
- [x] Capture visual evidence: `evidence/03_github/branches.png`, `evidence/03_github/commit_history.png`, `evidence/03_github/git_status.png`
- [ ] Connect and push to GitHub remote repository (Awaiting user URL confirmation)

---

## Stage 4: Docker Containerization & Docker Hub Publishing
- [x] Create Dockerfile for v1, v2, v3
- [x] Build Docker image: `thiru247/notification-system:v1` (ID: `d03c60aa3685`)
- [x] Build Docker image: `thiru247/notification-system:v2` (ID: `351b49bffaf4`)
- [x] Build Docker image: `thiru247/notification-system:v3` (ID: `8059f18fd22e`)
- [x] Verify image tags and IDs locally (`docker images`)
- [x] Save docker image verification to `evidence/06_docker/image_tags.txt` & `image_tags.png`
- [x] Run container for v1 and verify local CRUD (port 8091)
- [x] Run container for v2 and verify local CRUD & persistence (port 8092)
- [x] Run container for v3 and verify local CRUD & polished UI (port 8093)
- [x] Capture container test output in `evidence/06_docker/container_testing.txt` & `.png`
- [x] Test Docker Hub push and capture authorization challenge in `evidence/07_dockerhub/push_attempt.txt` & `.png`
- [ ] Complete remote push to Docker Hub (Awaiting user credentials/token)

---

## Stage 5: Kubernetes Orchestration & Deployment
- [x] Create Kubernetes manifests under `kubernetes/`:
  - `v1-deployment.yaml` & `v1-service.yaml` (port 8081, NodePort 30081)
  - `v2-deployment.yaml` & `v2-service.yaml` (port 8082, NodePort 30082)
  - `v3-deployment.yaml` & `v3-service.yaml` (port 8083, NodePort 30083)
  - Configured resource requests/limits, health checks (liveness/readiness), 2 replicas each
- [x] Deploy manifests to Kubernetes cluster
- [x] Import image tags into containerd `k8s.io` namespace
- [x] Verify Deployments status (`kubectl get deployments`)
- [x] Verify Pods readiness (`kubectl get pods` — all 6 pods 1/1 Running)
- [x] Verify Services configuration (`kubectl get services`)
- [x] Establish port routing / gateway:
  - `http://localhost:8081` -> v1
  - `http://localhost:8082` -> v2
  - `http://localhost:8083` -> v3
- [x] Verify live endpoints and execute Add, View, Delete operations on each localhost port
- [x] Capture Kubernetes evidence:
  - `evidence/08_kubernetes/deployments.png` & `.txt`
  - `evidence/08_kubernetes/pods.png` & `.txt`
  - `evidence/08_kubernetes/services.png` & `.txt`
  - `evidence/08_kubernetes/localhost_verification.png` & `.txt`
  - `evidence/09_browser_verification/v1_localhost.png`
  - `evidence/09_browser_verification/v2_localhost.png`
  - `evidence/09_browser_verification/v3_localhost.png`

---

## Stage 6: Jenkins CI/CD Pipeline
- [x] Create parameterized/branch-aware `Jenkinsfile` covering:
  - Checkout
  - Dependency Installation
  - Automated Tests Execution
  - Docker Image Build
  - Tagging
  - Docker Hub Authentication
  - Image Push
  - Build Status Reporting
- [x] Validate Jenkinsfile syntax and configuration
- [x] Start live Jenkins instance in Docker on port 8080
- [x] Save pipeline configurations and logs in `evidence/05_jenkins/`
- [x] Capture Jenkins visual evidence: `jenkins_web_ui.png`, `pipeline_config.png`, `pipeline_status.png`

---

## Stage 7: Evidence Index & Final Report
- [x] Maintain numbered evidence catalog in `evidence/README.md` (41 cataloged evidence items)
- [x] Generate comprehensive final report in `evidence/10_final_report/FINAL_REPORT.md`
- [x] Generate executive verification matrix screenshot `evidence/10_final_report/final_verification.png`
