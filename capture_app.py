import os
import sys
import time
import subprocess
import requests

def capture_app_screenshot(app_path, port, output_png, sample_notifs=None, extra_env=None):
    env = os.environ.copy()
    env["PORT"] = str(port)
    if extra_env:
        env.update(extra_env)

    # Launch app process
    proc = subprocess.Popen([sys.executable, app_path], env=env)
    url = f"http://127.0.0.1:{port}"

    try:
        # Wait for app to be responsive
        ready = False
        for _ in range(20):
            try:
                r = requests.get(f"{url}/health", timeout=1)
                if r.status_code == 200:
                    ready = True
                    break
            except Exception:
                time.sleep(0.5)

        if not ready:
            print(f"Server at {url} failed to start in time.")
            return False

        # Add sample notifications if provided
        if sample_notifs:
            for item in sample_notifs:
                requests.post(f"{url}/api/notifications", json=item, timeout=2)

        # Call screenshot
        screenshot_script = os.path.join(os.path.dirname(__file__), "take_screenshot.py")
        subprocess.run([sys.executable, screenshot_script, "url", f"{url}/", output_png], check=True)
        print(f"Captured screenshot for {app_path} at {output_png}")
        return True
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

if __name__ == "__main__":
    app_version = sys.argv[1] if len(sys.argv) > 1 else "v1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5001
    output = sys.argv[3] if len(sys.argv) > 3 else f"evidence/02_application/{app_version}_homepage.png"

    if app_version == "v1":
        app_path = "app/app.py"
    else:
        app_path = f"versions/{app_version}/app/app.py"

    samples = [
        {"title": f"System Alert [{app_version.upper()}]", "message": f"Notification service {app_version} operational check passed."}
    ]
    if app_version in ["v2", "v3"]:
        samples.append({
            "title": "Database Connection",
            "message": "Persistent SQLite storage verified and indexed successfully."
        })
    if app_version == "v3":
        samples.append({
            "title": "Cluster Health Warning",
            "message": "High memory consumption detected on worker node 2."
        })

    capture_app_screenshot(app_path, port, output, sample_notifs=samples)
