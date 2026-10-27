# DevOps Execution Checklist: Notification Management System

**Project Name:** Notification Management System  
**Engineer:** DevOps Engineer  
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
- [ ] Initialize and verify Docker Engine / daemon
- [ ] Inspect Kubernetes environment (kubectl v1.36.1, cluster readiness)
- [ ] Inspect Jenkins availability (service, local port 8080)
- [x] Save initial environment output to `evidence/01_environment/tool_versions.txt`
- [ ] Capture tool versions visual evidence / screenshot `evidence/01_environment/tool_versions.png`

---

## Stage 2: Application Development & Local Verification
### Version 1 (v1)
- [ ] Create v1 source code (`app.py`, basic in-memory CRUD, simple HTML UI)
- [ ] Create v1 HTML templates (`templates/index.html`) & CSS (`static/style.css`)
- [ ] Create `requirements.txt` for v1
- [ ] Create automated tests (`tests/test_app.py`) for v1:
  - Add notification (title & message)
  - View notifications (verify ID, title, message, timestamp)
  - Delete notification (by ID)
  - Empty notification handling
  - Nonexistent ID deletion handling
  - Invalid input handling
- [ ] Run automated tests for v1 and record output in `evidence/04_tests/v1_test_results.txt`
- [ ] Run v1 web application locally and verify CRUD
- [ ] Capture visual evidence: `evidence/02_application/v1_homepage.png`, `evidence/04_tests/v1_test_results.png`

### Version 2 (v2)
- [ ] Create v2 source code with improved UI, input validation, and SQLite persistent storage
- [ ] Create v2 HTML templates & styling
- [ ] Create automated tests for v2 (CRUD, persistence across requests, validation errors)
- [ ] Run automated tests for v2 and record output in `evidence/04_tests/v2_test_results.txt`
- [ ] Run v2 web application locally and verify CRUD & persistence
- [ ] Capture visual evidence: `evidence/02_application/v2_homepage.png`, `evidence/04_tests/v2_test_results.png`

### Version 3 (v3)
- [ ] Create v3 source code with advanced error handling, formatted timestamps, strict validation, status badges, and polished UI
- [ ] Create v3 HTML templates, modern styling, and flash alerts
- [ ] Create automated tests for v3 (all edge cases, error responses, validation, deletion)
- [ ] Run automated tests for v3 and record output in `evidence/04_tests/v3_test_results.txt`
- [ ] Run v3 web application locally and verify CRUD & polished UI
- [ ] Capture visual evidence: `evidence/02_application/v3_homepage.png`, `evidence/04_tests/v3_test_results.png`

---

## Stage 3: GitHub Version Control
- [ ] Initialize Git repository in the project folder
- [ ] Configure `.gitignore`
- [ ] Commit and branch `v1`
- [ ] Commit and branch `v2`
- [ ] Commit and branch `v3`
- [ ] Merge / align `main` branch
- [ ] Save git status, branch list, and commit log to `evidence/03_github/`
- [ ] Capture visual evidence: `evidence/03_github/branches.png`, `evidence/03_github/commit_history.png`
- [ ] Ask user for GitHub remote repository URL / confirm push authorization
- [ ] Push `main`, `v1`, `v2`, `v3` to GitHub remote
- [ ] Capture remote push confirmation in `evidence/03_github/`

---

## Stage 4: Docker Containerization & Docker Hub Publishing
- [ ] Create Dockerfile for v1, v2, v3
- [ ] Build Docker image: `thiru247/notification-system:v1`
- [ ] Build Docker image: `thiru247/notification-system:v2`
- [ ] Build Docker image: `thiru247/notification-system:v3`
- [ ] Verify image tags and IDs locally (`docker images`)
- [ ] Save docker image verification to `evidence/06_docker/image_tags.txt`
- [ ] Run container for v1 and verify local CRUD
- [ ] Run container for v2 and verify local CRUD & persistence
- [ ] Run container for v3 and verify local CRUD & polished UI
- [ ] Authenticate to Docker Hub securely
- [ ] Push `thiru247/notification-system:v1`, `:v2`, `:v3` to Docker Hub
- [ ] Verify published images on Docker Hub and record in `evidence/07_dockerhub/`
- [ ] Capture visual evidence: `evidence/06_docker/image_tags.png`, `evidence/07_dockerhub/published_tags.png`

---

## Stage 5: Kubernetes Orchestration & Deployment
- [ ] Create Kubernetes manifests under `kubernetes/`:
  - `v1-deployment.yaml` & `v1-service.yaml` (port 8081)
  - `v2-deployment.yaml` & `v2-service.yaml` (port 8082)
  - `v3-deployment.yaml` & `v3-service.yaml` (port 8083)
  - Configure resource requests/limits, health checks (liveness/readiness), replica counts
- [ ] Deploy manifests to Kubernetes cluster
- [ ] Verify Deployments status (`kubectl get deployments`)
- [ ] Verify Pods readiness (`kubectl get pods`)
- [ ] Verify Services configuration (`kubectl get services`)
- [ ] Establish port routing / port-forwarding:
  - `http://localhost:8081` -> v1
  - `http://localhost:8082` -> v2
  - `http://localhost:8083` -> v3
- [ ] Verify live endpoints and execute Add, View, Delete operations on each localhost port
- [ ] Capture Kubernetes evidence:
  - `evidence/08_kubernetes/deployments.png` & `.txt`
  - `evidence/08_kubernetes/pods.png` & `.txt`
  - `evidence/08_kubernetes/services.png` & `.txt`
  - `evidence/09_browser_verification/v1_localhost.png`
  - `evidence/09_browser_verification/v2_localhost.png`
  - `evidence/09_browser_verification/v3_localhost.png`

---

## Stage 6: Jenkins CI/CD Pipeline
- [ ] Create parameterized/branch-aware `Jenkinsfile` covering:
  - Checkout
  - Dependency Installation
  - Automated Tests Execution
  - Docker Image Build
  - Tagging
  - Docker Hub Authentication
  - Image Push
  - Build Status Reporting
- [ ] Validate Jenkinsfile syntax and configuration
- [ ] Check Jenkins server accessibility; trigger pipeline or document execution steps
- [ ] Save pipeline configurations and logs in `evidence/05_jenkins/`
- [ ] Capture Jenkins visual evidence

---

## Stage 7: Evidence Index & Final Report
- [ ] Maintain evidence index in `evidence/README.md`
- [ ] Generate comprehensive final report in `evidence/10_final_report/FINAL_REPORT.md`
- [ ] Include verification matrix with PASS/FAIL/BLOCKED statuses based on actual captured evidence
- [ ] Capture `evidence/10_final_report/final_verification.png`
