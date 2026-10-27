import time
import subprocess
import requests

def test_container(version, port):
    container_name = f"test-notif-{version}"
    image = f"thiru247/notification-system:{version}"
    print(f"\n==========================================")
    print(f"Testing Container: {image} on port {port}")
    print(f"==========================================")

    # Clean up previous container if any
    subprocess.run(["wsl", "-d", "Ubuntu", "docker", "rm", "-f", container_name], capture_output=True)

    # Run container
    run_res = subprocess.run([
        "wsl", "-d", "Ubuntu", "docker", "run", "-d",
        "--name", container_name,
        "-p", f"{port}:8080",
        image
    ], capture_output=True, text=True)
    cid = run_res.stdout.strip()[:12]
    print(f"Container started with ID: {cid}")

    base_url = f"http://127.0.0.1:{port}"
    # Wait for ready
    ready = False
    for _ in range(15):
        try:
            r = requests.get(f"{base_url}/health", timeout=1)
            if r.status_code == 200:
                ready = True
                print(f"Health check PASS: {r.json()}")
                break
        except Exception:
            time.sleep(0.5)

    if not ready:
        print("FAIL: Container failed health check.")
        return False

    # 1. VIEW (Initial Empty or existing)
    view_init = requests.get(f"{base_url}/api/notifications")
    print(f"1. VIEW initial state: {view_init.status_code} -> count: {len(view_init.json())}")

    # 2. ADD notification
    payload = {
        "title": f"Container Test Alert {version.upper()}",
        "message": f"Verified live container operations for {version} release."
    }
    if version == "v3":
        payload["priority"] = "CRITICAL"

    add_res = requests.post(f"{base_url}/api/notifications", json=payload)
    print(f"2. ADD notification: {add_res.status_code} -> {add_res.json()}")
    notif_id = add_res.json().get('id')

    # 3. VIEW verified
    view_res = requests.get(f"{base_url}/api/notifications")
    print(f"3. VIEW after add: {view_res.status_code} -> count: {len(view_res.json())}")

    # 4. DELETE notification
    del_res = requests.delete(f"{base_url}/api/notifications/{notif_id}")
    print(f"4. DELETE notification #{notif_id}: {del_res.status_code} -> {del_res.json()}")

    # 5. VIEW after delete
    view_final = requests.get(f"{base_url}/api/notifications")
    print(f"5. VIEW after delete: {view_final.status_code} -> count: {len(view_final.json())}")

    # Stop container
    subprocess.run(["wsl", "-d", "Ubuntu", "docker", "rm", "-f", container_name], capture_output=True)
    print(f"Container {container_name} cleaned up.")
    return True

if __name__ == "__main__":
    v1_ok = test_container("v1", 8091)
    v2_ok = test_container("v2", 8092)
    v3_ok = test_container("v3", 8093)
    print("\nAll Container CRUD verification complete!")
