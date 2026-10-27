import sys
from playwright.sync_api import sync_playwright

def capture(url, output_png):
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe", headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 850})
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(2000)
        page.screenshot(path=output_png, full_page=False)
        browser.close()
        print(f"Captured: {output_png}")

if __name__ == "__main__":
    capture(sys.argv[1], sys.argv[2])
