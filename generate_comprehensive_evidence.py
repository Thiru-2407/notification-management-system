import subprocess
import os
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

BASE_DIR = r"C:\Users\thiru\.gemini\antigravity\scratch\notification-management-system"
EVIDENCE_DIR = os.path.join(BASE_DIR, "evidence")

def render_terminal_png(text, out_png, title="Terminal"):
    lines = text.strip().splitlines()
    if not lines:
        lines = ["(No content)"]
    if len(lines) > 85:
        lines = lines[:85] + ["... (truncated for view) ..."]
    
    font = ImageFont.load_default()
    char_w = 7
    char_h = 14
    max_len = max(len(l) for l in lines)
    width = max(860, max_len * char_w + 60)
    height = len(lines) * char_h + 80

    img = Image.new("RGB", (width, height), color=(24, 24, 27))
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (width, 36)], fill=(39, 39, 42))
    draw.ellipse([(14, 12), (24, 22)], fill=(239, 68, 68))
    draw.ellipse([(32, 12), (42, 22)], fill=(234, 179, 8))
    draw.ellipse([(50, 12), (60, 22)], fill=(34, 197, 94))
    draw.text((75, 11), title, fill=(212, 212, 216), font=font)

    y = 50
    for line in lines:
        color = (228, 228, 231)
        if "=== " in line or "--- " in line or line.startswith("["):
            color = (56, 189, 248)
        elif "PASS" in line or "passed" in line or "Running" in line or "Ready" in line or "healthy" in line:
            color = (74, 222, 128)
        elif "FAIL" in line or "failed" in line or "ERROR" in line or "Error" in line:
            color = (248, 113, 113)
        elif "WARN" in line or "Warning" in line:
            color = (250, 204, 21)
        draw.text((25, y), line, fill=color, font=font)
        y += char_h
    
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    img.save(out_png)
    print(f"[Terminal] Saved: {out_png}")

def run_cmd(cmd, shell=True):
    res = subprocess.run(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    return res.stdout

def main():
    print("=== Generating Comprehensive Evidence ===")

    # 1. VS Code Details
    print("\n--- 1. VS Code Evidence ---")
    ext_out = run_cmd("code --list-extensions --show-versions")
    ws_tree = run_cmd(f"powershell -Command \"Get-ChildItem -Path '{BASE_DIR}' -Exclude .git, __pycache__, .pytest_cache | Select-Object FullName, Length | Format-Table -AutoSize\"")
    combined_vscode = f"=== VS CODE EXTENSIONS INSTALLED ===\n{ext_out}\n\n=== VS CODE WORKSPACE DIRECTORY STRUCTURE ===\n{ws_tree}"
    
    txt_path = os.path.join(EVIDENCE_DIR, "01_environment", "vscode_extensions_and_workspace.txt")
    png_path = os.path.join(EVIDENCE_DIR, "01_environment", "vscode_extensions_and_workspace.png")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(combined_vscode)
    render_terminal_png(combined_vscode, png_path, "VS Code Workspace & Extensions")

    # 2. Jenkins Container Logs & Status
    print("\n--- 2. Jenkins Evidence ---")
    jenkins_logs = run_cmd("wsl -d Ubuntu docker logs --tail 60 jenkins")
    txt_path = os.path.join(EVIDENCE_DIR, "05_jenkins", "jenkins_container_logs.txt")
    png_path = os.path.join(EVIDENCE_DIR, "05_jenkins", "jenkins_container_logs.png")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(jenkins_logs)
    render_terminal_png(jenkins_logs, png_path, "Jenkins Container Runtime Logs (localhost:8080)")

    # 3. Docker Evidence
    print("\n--- 3. Docker Evidence ---")
    docker_ps_out = run_cmd("wsl -d Ubuntu docker ps -a")
    txt_path = os.path.join(EVIDENCE_DIR, "06_docker", "docker_ps.txt")
    png_path = os.path.join(EVIDENCE_DIR, "06_docker", "docker_ps.png")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(docker_ps_out)
    render_terminal_png(docker_ps_out, png_path, "Docker Process Status (docker ps -a)")

    docker_inspect = run_cmd("wsl -d Ubuntu docker inspect thiru247/notification-system:v1 thiru247/notification-system:v2 thiru247/notification-system:v3 --format 'Image: {{.RepoTags}} | Created: {{.Created}} | Arch: {{.Architecture}} | Size: {{.Size}}'")
    txt_path = os.path.join(EVIDENCE_DIR, "06_docker", "docker_inspect.txt")
    png_path = os.path.join(EVIDENCE_DIR, "06_docker", "docker_inspect.png")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(docker_inspect)
    render_terminal_png(docker_inspect, png_path, "Docker Image Metadata & Architecture Inspect")

    # 4. Kubernetes Evidence
    print("\n--- 4. Kubernetes Evidence ---")
    k8s_all = run_cmd("kubectl get all -o wide")
    txt_path = os.path.join(EVIDENCE_DIR, "08_kubernetes", "all_resources_wide.txt")
    png_path = os.path.join(EVIDENCE_DIR, "08_kubernetes", "all_resources_wide.png")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(k8s_all)
    render_terminal_png(k8s_all, png_path, "Kubernetes Cluster Resources (kubectl get all -o wide)")

    k8s_v1_logs = run_cmd("kubectl logs -l app=notification-v1 --tail 30")
    txt_path = os.path.join(EVIDENCE_DIR, "08_kubernetes", "pod_logs_v1.txt")
    png_path = os.path.join(EVIDENCE_DIR, "08_kubernetes", "pod_logs_v1.png")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(k8s_v1_logs)
    render_terminal_png(k8s_v1_logs, png_path, "Kubernetes v1 Pod Logs (notification-v1)")

    k8s_v2_logs = run_cmd("kubectl logs -l app=notification-v2 --tail 30")
    txt_path = os.path.join(EVIDENCE_DIR, "08_kubernetes", "pod_logs_v2.txt")
    png_path = os.path.join(EVIDENCE_DIR, "08_kubernetes", "pod_logs_v2.png")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(k8s_v2_logs)
    render_terminal_png(k8s_v2_logs, png_path, "Kubernetes v2 Pod Logs (notification-v2)")

    # 5. Playwright Live Browser Interaction for CRUD operations
    print("\n--- 5. Playwright Browser CRUD Verification ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe", headless=True)

        # 5a. Jenkins Live Web UI
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 850})
            page.goto("http://localhost:8080/login", wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(2000)
            jenkins_png = os.path.join(EVIDENCE_DIR, "05_jenkins", "jenkins_live_login_ui.png")
            page.screenshot(path=jenkins_png)
            print(f"[Browser] Saved Jenkins live UI: {jenkins_png}")
            page.close()
        except Exception as e:
            print(f"Error capturing Jenkins live UI: {e}")

        # 5b. v1 CRUD: Add notification & capture
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 850})
            page.goto("http://localhost:8081/", wait_until="domcontentloaded", timeout=10000)
            page.fill("input[name='title']", "Kubernetes Production Deployment v1")
            page.fill("textarea[name='message']", "Verified live pod execution on port 8081.")
            page.click("button[type='submit']")
            page.wait_for_timeout(1500)
            v1_crud_png = os.path.join(EVIDENCE_DIR, "09_browser_verification", "v1_crud_notification_added.png")
            page.screenshot(path=v1_crud_png)
            print(f"[Browser] Saved v1 CRUD screenshot: {v1_crud_png}")
            page.close()
        except Exception as e:
            print(f"Error on v1 browser CRUD: {e}")

        # 5c. v2 CRUD: Add notification with SQLite validation & capture
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 850})
            page.goto("http://localhost:8082/", wait_until="domcontentloaded", timeout=10000)
            page.fill("input[name='title']", "SQLite Persistent Storage Check v2")
            page.fill("textarea[name='message']", "Verified database isolation and input length constraints.")
            page.click("button[type='submit']")
            page.wait_for_timeout(1500)
            v2_crud_png = os.path.join(EVIDENCE_DIR, "09_browser_verification", "v2_crud_notification_added.png")
            page.screenshot(path=v2_crud_png)
            print(f"[Browser] Saved v2 CRUD screenshot: {v2_crud_png}")
            page.close()
        except Exception as e:
            print(f"Error on v2 browser CRUD: {e}")

        # 5d. v3 CRUD: Add notification with CRITICAL priority & capture
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 850})
            page.goto("http://localhost:8083/", wait_until="domcontentloaded", timeout=10000)
            page.fill("input[name='title']", "Critical Cluster Health Alert v3")
            page.fill("textarea[name='message']", "All 6 Kubernetes pods running across 3 independent versions.")
            page.select_option("select[name='priority']", "CRITICAL")
            page.click("button[type='submit']")
            page.wait_for_timeout(1500)
            v3_crud_png = os.path.join(EVIDENCE_DIR, "09_browser_verification", "v3_crud_notification_added.png")
            page.screenshot(path=v3_crud_png)
            print(f"[Browser] Saved v3 CRUD screenshot: {v3_crud_png}")

            # Now delete the notification in v3 to prove deletion in browser UI
            del_buttons = page.query_selector_all("button.btn-delete, button.btn-danger, form[action*='delete'] button")
            if del_buttons:
                del_buttons[-1].click()
                page.wait_for_timeout(1500)
                v3_del_png = os.path.join(EVIDENCE_DIR, "09_browser_verification", "v3_crud_notification_deleted.png")
                page.screenshot(path=v3_del_png)
                print(f"[Browser] Saved v3 CRUD deletion screenshot: {v3_del_png}")
            page.close()
        except Exception as e:
            print(f"Error on v3 browser CRUD: {e}")

        browser.close()

    print("\n=== Comprehensive evidence generation complete ===")

if __name__ == "__main__":
    main()
