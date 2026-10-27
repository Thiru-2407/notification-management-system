import time
import requests
import subprocess
import os

def test_endpoint(version, port):
    url = f"http://127.0.0.1:{port}"
    print(f"\n=======================================================")
    print(f"VERIFYING KUBERNETES ENDPOINT: {version.upper()} at {url}")
    print(f"=======================================================")

    # 1. Health check
    try:
        r = requests.get(f"{url}/health", timeout=3)
        print(f"Health check [GET /health]: HTTP {r.status_code}")
        print(f"Response: {r.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

    # 2. View initial notifications
    r_view = requests.get(f"{url}/api/notifications")
    print(f"View alerts [GET /api/notifications]: HTTP {r_view.status_code} ({len(r_view.json())} alerts)")

    # 3. Add notification via REST
    payload = {
        "title": f"K8s Live Deployment Verification {version.upper()}",
        "message": f"Successfully verified Kubernetes Pods and Service routing on port {port}."
    }
    if version == "v3":
        payload["priority"] = "SUCCESS"

    r_add = requests.post(f"{url}/api/notifications", json=payload)
    print(f"Add alert [POST /api/notifications]: HTTP {r_add.status_code}")
    print(f"Created: {r_add.json()}")
    created_id = r_add.json().get('id')

    # 4. View notifications after creation
    r_view2 = requests.get(f"{url}/api/notifications")
    print(f"View alerts after add: count = {len(r_view2.json())}")

    # 5. Capture browser screenshot of localhost URL
    png_path = f"evidence/09_browser_verification/{version}_localhost.png"
    screenshot_cmd = ["python", "take_screenshot.py", "url", f"{url}/", png_path]
    subprocess.run(screenshot_cmd)
    print(f"Captured screenshot at {png_path}")

    # 6. Delete notification
    if created_id:
        r_del = requests.delete(f"{url}/api/notifications/{created_id}")
        print(f"Delete alert #{created_id} [DELETE /api/notifications/{created_id}]: HTTP {r_del.status_code}")
        print(f"Delete response: {r_del.json()}")

    return True

if __name__ == "__main__":
    v1 = test_endpoint("v1", 8081)
    v2 = test_endpoint("v2", 8082)
    v3 = test_endpoint("v3", 8083)
    print("\nAll Kubernetes localhost verifications completed.")
