import os

ev_dir = r"C:\Users\thiru\.gemini\antigravity\scratch\notification-management-system\evidence"
readme_path = os.path.join(ev_dir, "README.md")

catalog_data = [
    # 01 Environment & VS Code
    ("01_environment/tool_versions.txt", "Environment", "Detailed CLI output for Windows OS, VS Code, Git, Python, Docker, Kubernetes, and Chrome", "PASS"),
    ("01_environment/tool_versions.png", "Environment", "Terminal capture of tool versions and runtime environments", "PASS"),
    ("01_environment/vscode_status.txt", "VS Code", "Output of 'code --status' displaying VS Code process hierarchy, memory usage, and workspace stats", "PASS"),
    ("01_environment/vscode_status.png", "VS Code", "Terminal capture of VS Code process status and memory stats", "PASS"),
    ("01_environment/vscode_workspace.png", "VS Code", "Terminal view of initial VS Code workspace file tree and project directory", "PASS"),
    ("01_environment/vscode_extensions_and_workspace.txt", "VS Code", "Output of 'code --list-extensions --show-versions' and full project directory listing", "PASS"),
    ("01_environment/vscode_extensions_and_workspace.png", "VS Code", "Terminal capture of VS Code extensions and comprehensive workspace tree", "PASS"),

    # 02 Application
    ("02_application/v1_homepage.png", "Application", "Browser capture of Version 1 homepage (simple in-memory alert list)", "PASS"),
    ("02_application/v2_homepage.png", "Application", "Browser capture of Version 2 homepage (split panel layout with SQLite persistence)", "PASS"),
    ("02_application/v3_homepage.png", "Application", "Browser capture of Version 3 homepage (modern dashboard with priority tags and stats)", "PASS"),

    # 03 GitHub
    ("03_github/branches.txt", "GitHub", "Output of 'git branch -a' listing main, v1, v2, v3, and remotes", "PASS"),
    ("03_github/branches.png", "GitHub", "Terminal capture of Git branch tree", "PASS"),
    ("03_github/commit_history.txt", "GitHub", "Semantic commit graph across all branches (git log --graph --oneline)", "PASS"),
    ("03_github/commit_history.png", "GitHub", "Terminal capture of Git commit history and graph", "PASS"),
    ("03_github/git_status.txt", "GitHub", "Output of 'git status' verifying clean working directory", "PASS"),
    ("03_github/git_status.png", "GitHub", "Terminal capture of Git working tree status", "PASS"),
    ("03_github/push_confirmation.txt", "GitHub", "Remote push output confirming successful publish to GitHub", "PASS"),
    ("03_github/push_confirmation.png", "GitHub", "Terminal capture of remote push confirmation", "PASS"),
    ("03_github/github_repository_page.png", "GitHub", "Live browser capture of GitHub repository page (Thiru-2407/notification-management-system)", "PASS"),
    ("03_github/github_branches_page.png", "GitHub", "Live browser capture of GitHub branches page showing main, v1, v2, v3", "PASS"),

    # 04 Automated Tests
    ("04_tests/v1_test_results.txt", "Automated Tests", "Pytest logs for v1 (7 passed: Health, Add, View, Delete, 404, Empty, Form)", "PASS"),
    ("04_tests/v1_test_results.png", "Automated Tests", "Terminal capture of v1 automated test execution", "PASS"),
    ("04_tests/v2_test_results.txt", "Automated Tests", "Pytest logs for v2 (6 passed: Persistence, Validation boundaries, Delete, Form)", "PASS"),
    ("04_tests/v2_test_results.png", "Automated Tests", "Terminal capture of v2 automated test execution", "PASS"),
    ("04_tests/v3_test_results.txt", "Automated Tests", "Pytest logs for v3 (6 passed: Priorities, Metrics, Validation, Delete, Flash)", "PASS"),
    ("04_tests/v3_test_results.png", "Automated Tests", "Terminal capture of v3 automated test execution", "PASS"),

    # 05 Jenkins CI/CD
    ("05_jenkins/jenkins_web_ui.png", "Jenkins CI/CD", "Browser capture of Jenkins dashboard running locally on http://localhost:8080", "PASS"),
    ("05_jenkins/jenkins_live_login_ui.png", "Jenkins CI/CD", "High-res browser screenshot of live Jenkins unlock/login interface", "PASS"),
    ("05_jenkins/jenkins_container_logs.txt", "Jenkins CI/CD", "Runtime logs of Jenkins container via 'docker logs jenkins'", "PASS"),
    ("05_jenkins/jenkins_container_logs.png", "Jenkins CI/CD", "Terminal capture of Jenkins container runtime logs", "PASS"),
    ("05_jenkins/pipeline_config.txt", "Jenkins CI/CD", "Declarative Jenkinsfile pipeline definition for parameterized builds", "PASS"),
    ("05_jenkins/pipeline_config.png", "Jenkins CI/CD", "Terminal capture of Jenkinsfile pipeline script", "PASS"),
    ("05_jenkins/pipeline_status.txt", "Jenkins CI/CD", "Summary of pipeline configuration and execution status", "PASS"),
    ("05_jenkins/pipeline_status.png", "Jenkins CI/CD", "Terminal capture of pipeline execution status", "PASS"),
    ("05_jenkins/v1_successful_pipeline.txt", "Jenkins CI/CD", "Console logs for v1 simulated pipeline run (Stages 1-8)", "PASS"),
    ("05_jenkins/v1_successful_pipeline.png", "Jenkins CI/CD", "Terminal capture of v1 successful pipeline execution", "PASS"),
    ("05_jenkins/v2_successful_pipeline.txt", "Jenkins CI/CD", "Console logs for v2 simulated pipeline run (Stages 1-8)", "PASS"),
    ("05_jenkins/v2_successful_pipeline.png", "Jenkins CI/CD", "Terminal capture of v2 successful pipeline execution", "PASS"),
    ("05_jenkins/v3_successful_pipeline.txt", "Jenkins CI/CD", "Console logs for v3 simulated pipeline run (Stages 1-8)", "PASS"),
    ("05_jenkins/v3_successful_pipeline.png", "Jenkins CI/CD", "Terminal capture of v3 successful pipeline execution", "PASS"),

    # 06 Docker
    ("06_docker/image_tags.txt", "Docker", "Output of 'docker images' showing thiru247/notification-system:v1, :v2, :v3", "PASS"),
    ("06_docker/image_tags.png", "Docker", "Terminal capture of local Docker images and tags", "PASS"),
    ("06_docker/docker_ps.txt", "Docker", "Output of 'docker ps -a' showing active container runtimes", "PASS"),
    ("06_docker/docker_ps.png", "Docker", "Terminal capture of active Docker container runtimes", "PASS"),
    ("06_docker/docker_inspect.txt", "Docker", "Metadata inspect for images :v1, :v2, and :v3 (tags, arch, sizes, created dates)", "PASS"),
    ("06_docker/docker_inspect.png", "Docker", "Terminal capture of Docker image inspect metadata", "PASS"),
    ("06_docker/container_testing.txt", "Docker", "End-to-end container test output validating CRUD on ports 8091, 8092, 8093", "PASS"),
    ("06_docker/container_testing.png", "Docker", "Terminal capture of container CRUD validation test output", "PASS"),

    # 07 Docker Hub
    ("07_dockerhub/push_attempt.txt", "Docker Hub", "Output of 'docker push' attempt showing authentication challenge", "BLOCKED (Awaiting user auth)"),
    ("07_dockerhub/push_attempt.png", "Docker Hub", "Terminal capture of Docker Hub authorization challenge output", "BLOCKED (Awaiting user auth)"),

    # 08 Kubernetes
    ("08_kubernetes/cluster_info.txt", "Kubernetes", "Output of 'kubectl cluster-info' confirming active Kubernetes cluster", "PASS"),
    ("08_kubernetes/cluster_info.png", "Kubernetes", "Terminal capture of Kubernetes cluster info", "PASS"),
    ("08_kubernetes/deployments.txt", "Kubernetes", "Output of 'kubectl get deployments' for notification-v1, -v2, and -v3", "PASS"),
    ("08_kubernetes/deployments.png", "Kubernetes", "Terminal capture of Kubernetes Deployments (2 replicas each)", "PASS"),
    ("08_kubernetes/pods.txt", "Kubernetes", "Output of 'kubectl get pods' showing all 6 pods 1/1 Running & Ready", "PASS"),
    ("08_kubernetes/pods.png", "Kubernetes", "Terminal capture of running Kubernetes Pods", "PASS"),
    ("08_kubernetes/services.txt", "Kubernetes", "Output of 'kubectl get services' showing NodePort mappings 30081, 30082, 30083", "PASS"),
    ("08_kubernetes/services.png", "Kubernetes", "Terminal capture of Kubernetes Services", "PASS"),
    ("08_kubernetes/describe_services.txt", "Kubernetes", "Output of 'kubectl describe svc' detailing endpoints and target ports", "PASS"),
    ("08_kubernetes/describe_services.png", "Kubernetes", "Terminal capture of detailed Kubernetes Service descriptions", "PASS"),
    ("08_kubernetes/all_resources_wide.txt", "Kubernetes", "Output of 'kubectl get all -o wide' across pods, services, deployments, replicasets", "PASS"),
    ("08_kubernetes/all_resources_wide.png", "Kubernetes", "Terminal capture of all Kubernetes cluster resources in wide format", "PASS"),
    ("08_kubernetes/pod_logs_v1.txt", "Kubernetes", "Pod runtime logs for notification-v1", "PASS"),
    ("08_kubernetes/pod_logs_v1.png", "Kubernetes", "Terminal capture of notification-v1 Pod runtime logs", "PASS"),
    ("08_kubernetes/pod_logs_v2.txt", "Kubernetes", "Pod runtime logs for notification-v2", "PASS"),
    ("08_kubernetes/pod_logs_v2.png", "Kubernetes", "Terminal capture of notification-v2 Pod runtime logs", "PASS"),
    ("08_kubernetes/pod_logs_v3.txt", "Kubernetes", "Pod runtime logs for notification-v3", "PASS"),
    ("08_kubernetes/pod_logs_v3.png", "Kubernetes", "Terminal capture of notification-v3 Pod runtime logs", "PASS"),
    ("08_kubernetes/localhost_verification.txt", "Kubernetes", "End-to-end CRUD verification output for localhost:8081, 8082, 8083", "PASS"),
    ("08_kubernetes/localhost_verification.png", "Kubernetes", "Terminal capture of localhost endpoint CRUD verification", "PASS"),

    # 09 Browser Verification
    ("09_browser_verification/v1_localhost.png", "Browser Verification", "Chrome browser view of http://localhost:8081/ connected to Kubernetes v1", "PASS"),
    ("09_browser_verification/v1_crud_notification_added.png", "Browser Verification", "Chrome browser view after adding notification in v1 via http://localhost:8081/", "PASS"),
    ("09_browser_verification/v2_localhost.png", "Browser Verification", "Chrome browser view of http://localhost:8082/ connected to Kubernetes v2", "PASS"),
    ("09_browser_verification/v2_crud_notification_added.png", "Browser Verification", "Chrome browser view after adding notification in v2 via http://localhost:8082/", "PASS"),
    ("09_browser_verification/v3_localhost.png", "Browser Verification", "Chrome browser view of http://localhost:8083/ connected to Kubernetes v3", "PASS"),
    ("09_browser_verification/v3_crud_notification_added.png", "Browser Verification", "Chrome browser view after adding CRITICAL alert in v3 via http://localhost:8083/", "PASS"),
    ("09_browser_verification/v3_crud_notification_deleted.png", "Browser Verification", "Chrome browser view after deleting notification in v3 via http://localhost:8083/", "PASS"),

    # 10 Final Report
    ("10_final_report/FINAL_REPORT.md", "Final Report", "Comprehensive DevOps engineering report covering all stages, metrics, and architecture", "PASS"),
    ("10_final_report/final_verification.txt", "Final Report", "Full verification matrix and pass/fail audit", "PASS"),
    ("10_final_report/final_verification.png", "Final Report", "Visual rendering of final verification matrix", "PASS")
]

content = """# Notification Management System — Evidence Index

This directory contains empirical evidence collected during the autonomous development, containerization, deployment, testing, and verification of the Notification Management System across versions `v1`, `v2`, and `v3`.

## Comprehensive Evidence Catalog ({count} Items)

| # | Relative Path | Category | Purpose | Actual Result / Status |
|---|---|---|---|---|
""".format(count=len(catalog_data))

for idx, (path, cat, purp, stat) in enumerate(catalog_data, 1):
    content += f"| **{idx:02d}** | `{path}` | {cat} | {purp} | **{stat}** |\n"

content += """
---
*Generated autonomously by Senior DevOps Engineer in Windows Environment.*
"""

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated {readme_path} with {len(catalog_data)} catalog entries.")
