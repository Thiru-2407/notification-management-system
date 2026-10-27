import sys
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

def render_terminal_screenshot(text_content, output_png, title="Terminal"):
    # Split lines
    lines = text_content.strip().splitlines()
    if not lines:
        lines = ["(No content)"]
    
    # Cap lines if too long
    if len(lines) > 80:
        lines = lines[:80] + ["... (truncated for screenshot) ..."]

    font = ImageFont.load_default()
    
    char_w = 7
    char_h = 14
    max_len = max(len(l) for l in lines)
    width = max(800, max_len * char_w + 60)
    height = len(lines) * char_h + 80

    img = Image.new("RGB", (width, height), color=(24, 24, 27))
    draw = ImageDraw.Draw(img)

    # Top title bar
    draw.rectangle([(0, 0), (width, 36)], fill=(39, 39, 42))
    # Red, yellow, green window buttons
    draw.ellipse([(14, 12), (24, 22)], fill=(239, 68, 68))
    draw.ellipse([(32, 12), (42, 22)], fill=(234, 179, 8))
    draw.ellipse([(50, 12), (60, 22)], fill=(34, 197, 94))
    
    # Title text
    draw.text((75, 11), title, fill=(212, 212, 216), font=font)

    # Render lines
    y = 50
    for line in lines:
        color = (228, 228, 231)
        if "=== " in line or "--- " in line or line.startswith("["):
            color = (56, 189, 248) # cyan
        elif "PASS" in line or "passed" in line or "True" in line or "Ready" in line:
            color = (74, 222, 128) # green
        elif "FAIL" in line or "failed" in line or "ERROR" in line or "Error" in line:
            color = (248, 113, 113) # red
        elif "WARN" in line or "Warning" in line:
            color = (250, 204, 21) # yellow
        
        draw.text((25, y), line, fill=color, font=font)
        y += char_h

    os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
    img.save(output_png)
    print(f"Terminal screenshot saved to {output_png}")

def capture_url(url, output_png):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    browser = chrome_path if os.path.exists(chrome_path) else edge_path

    abs_output = os.path.abspath(output_png)
    os.makedirs(os.path.dirname(abs_output), exist_ok=True)
    
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--hide-scrollbars",
        f"--screenshot={abs_output}",
        "--window-size=1280,850",
        url
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        print(f"Warning: Screenshot process timed out for {url}")
        return False
    if os.path.exists(abs_output):
        print(f"Browser screenshot saved to {abs_output}")
        return True
    else:
        print(f"Failed to capture screenshot: {res.stderr}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python take_screenshot.py url <url> <output_png> OR python take_screenshot.py text <text_file> <output_png> [title]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "url":
        capture_url(sys.argv[2], sys.argv[3])
    elif mode == "text":
        try:
            with open(sys.argv[2], "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(sys.argv[2], "r", encoding="utf-16", errors="ignore") as f:
                content = f.read()
        title = sys.argv[4] if len(sys.argv) > 4 else "Terminal Output"
        render_terminal_screenshot(content, sys.argv[3], title)
