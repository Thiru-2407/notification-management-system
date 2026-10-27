# Notification Management System — Evidence Index

This directory contains genuine, empirical evidence collected during the autonomous development, containerization, deployment, testing, and verification of the Notification Management System across versions `v1`, `v2`, and `v3`.

## Numbered Evidence Catalog

| # | Relative Path | Category | Purpose | Actual Result / Status |
|---|---|---|---|---|
| **01** | `01_environment/tool_versions.txt` | Environment | Records OS, VS Code, Git, Python, Docker, Kubernetes, and browser versions. | **PASS** — Captured real versions for all installed development tools. |
| **02** | `01_environment/tool_versions.png` | Environment | Visual screenshot representation of tool versions. | **PASS** — Rendered and verified. |
| **03** | `02_application/v1_homepage.png` | Application | Web UI capture of Version 1 running on local port. | **PASS** — Displays v1 minimalist alert table and submission form. |
| **04** | `02_application/v2_homepage.png` | Application | Web UI capture of Version 2 running on local port. | **PASS** — Displays v2 split-panel layout, card feed, and badge indicator. |
| **05** | `02_application/v3_homepage.png` | Application | Web UI capture of Version 3 running on local port. | **PASS** — Displays v3 polished dashboard with priority indicators and live stats. |
| **06** | `03_github/branches.txt` | Git / GitHub | Output of `git branch -a` listing `main`, `v1`, `v2`, and `v3`. | **PASS** — All 4 branches distinct and verified. |
| **07** | `03_github/branches.png` | Git / GitHub | Visual terminal capture of git branch tree. | **PASS** — Rendered and verified. |
| **08** | `03_github/commit_history.txt` | Git / GitHub | Output of `git log --graph --oneline --decorate --all`. | **PASS** — Distinct semantic commits for v1, v2, v3, and deployment manifests. |
| **09** | `03_github/commit_history.png` | Git / GitHub | Visual terminal capture of git commit graph. | **PASS** — Rendered and verified. |
| **10** | `03_github/git_status.txt` | Git / GitHub | Output of `git status` confirming clean working tree on `main`. | **PASS** — Clean working directory verified. |
| **11** | `03_github/git_status.png` | Git / GitHub | Visual screenshot of git status output. | **PASS** — Rendered and verified. |
| **12** | `04_tests/v1_test_results.txt` | Testing | Pytest test execution logs for Version 1 test suite. | **PASS** — 7 passed out of 7 (health, add, empty, invalid, delete, 404, form). |
| **13** | `04_tests/v1_test_results.png` | Testing | Visual terminal capture of v1 pytest execution. | **PASS** — Rendered and verified. |
| **14** | `04_tests/v2_test_results.txt` | Testing | Pytest test execution logs for Version 2 test suite. | **PASS** — 6 passed out of 6 (health, persistence, validation limits, delete, form). |
| **15** | `04_tests/v2_test_results.png` | Testing | Visual terminal capture of v2 pytest execution. | **PASS** — Rendered and verified. |
| **16** | `04_tests/v3_test_results.txt` | Testing | Pytest test execution logs for Version 3 test suite. | **PASS** — 6 passed out of 6 (health, stats, priorities, validation, delete, flash). |
| **17** | `04_tests/v3_test_results.png` | Testing | Visual terminal capture of v3 pytest execution. | **PASS** — Rendered and verified. |
| **18** | `05_jenkins/jenkins_web_ui.png` | CI/CD | Headless browser screenshot of live Jenkins server. | **PASS** — Captured active Jenkins instance on `http://localhost:8080`. |
| **19** | `05_jenkins/pipeline_config.txt` | CI/CD | Declarative `Jenkinsfile` configuration. | **PASS** — Covers multi-branch checkout, test, build, tag, auth, and push. |
| **20** | `05_jenkins/pipeline_config.png` | CI/CD | Visual rendering of Jenkins pipeline definition. | **PASS** — Rendered and verified. |
| **21** | `05_jenkins/pipeline_status.txt` | CI/CD | Summary of Jenkins pipeline stages and container run info. | **PASS** — Documented and verified. |
| **22** | `05_jenkins/pipeline_status.png` | CI/CD | Visual rendering of Jenkins configuration summary. | **PASS** — Rendered and verified. |
| **23** | `06_docker/image_tags.txt` | Docker | Output of `docker images` for `thiru247/notification-system`. | **PASS** — Image tags `:v1`, `:v2`, `:v3` built and verified locally. |
| **24** | `06_docker/image_tags.png` | Docker | Visual terminal capture of local Docker images. | **PASS** — Rendered and verified. |
| **25** | `06_docker/container_testing.txt` | Docker | End-to-end container test logs (Health, Add, View, Delete). | **PASS** — All 3 containers passed live CRUD testing on isolated ports. |
| **26** | `06_docker/container_testing.png` | Docker | Visual rendering of container CRUD test output. | **PASS** — Rendered and verified. |
| **27** | `07_dockerhub/push_attempt.txt` | Docker Hub | Command output of `docker push` attempt. | **BLOCKED** — Insufficient scope (requires user authentication token). |
| **28** | `07_dockerhub/push_attempt.png` | Docker Hub | Visual terminal capture of Docker Hub authorization challenge. | **BLOCKED** — Captured real authorization challenge. |
| **29** | `08_kubernetes/deployments.txt` | Kubernetes | Output of `kubectl get deployments -o wide`. | **PASS** — `notification-v1`, `notification-v2`, `notification-v3` deployed. |
| **30** | `08_kubernetes/deployments.png` | Kubernetes | Visual terminal capture of active Kubernetes Deployments. | **PASS** — Rendered and verified. |
| **31** | `08_kubernetes/pods.txt` | Kubernetes | Output of `kubectl get pods -o wide`. | **PASS** — All 6 Pods (2 replicas each) 1/1 Running and Healthy. |
| **32** | `08_kubernetes/pods.png` | Kubernetes | Visual terminal capture of running Kubernetes Pods. | **PASS** — Rendered and verified. |
| **33** | `08_kubernetes/services.txt` | Kubernetes | Output of `kubectl get services -o wide`. | **PASS** — Services `notification-v1-service`, `v2`, `v3` mapped to NodePorts. |
| **34** | `08_kubernetes/services.png` | Kubernetes | Visual terminal capture of Kubernetes Services. | **PASS** — Rendered and verified. |
| **35** | `08_kubernetes/localhost_verification.txt` | Kubernetes | Output of localhost end-to-end CRUD verification via ports 8081, 8082, 8083. | **PASS** — Health checks, Add, View, and Delete validated on each localhost port. |
| **36** | `08_kubernetes/localhost_verification.png` | Kubernetes | Visual terminal capture of localhost endpoint verification. | **PASS** — Rendered and verified. |
| **37** | `09_browser_verification/v1_localhost.png` | Browser Verification | Real Chrome browser screenshot of `http://localhost:8081/` routed to Kubernetes v1. | **PASS** — Real browser rendering with active alert. |
| **38** | `09_browser_verification/v2_localhost.png` | Browser Verification | Real Chrome browser screenshot of `http://localhost:8082/` routed to Kubernetes v2. | **PASS** — Real browser rendering with active alert. |
| **39** | `09_browser_verification/v3_localhost.png` | Browser Verification | Real Chrome browser screenshot of `http://localhost:8083/` routed to Kubernetes v3. | **PASS** — Real browser rendering with active alert and live metrics. |
| **40** | `10_final_report/FINAL_REPORT.md` | Final Report | Comprehensive DevOps engineering final report and verification matrix. | **PASS** — Complete documentation. |
| **41** | `10_final_report/final_verification.png` | Final Report | Executive verification matrix screenshot. | **PASS** — Rendered and verified. |
