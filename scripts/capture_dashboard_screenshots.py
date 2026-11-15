"""
MONSOON PULSE — Headless Screenshot Capture
Spins up a custom HTTP server for frontend/dist supporting /monsoon_pulse/ base path
and uses msedge headless to capture authentic full-resolution screenshots.
"""

import subprocess
import time
import socket
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = PROJECT_ROOT / "frontend" / "dist"
ASSETS_DIR = PROJECT_ROOT / "presentation_assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


class BaseUrlHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Strip '/monsoon_pulse' prefix if present
        clean_path = path
        if clean_path.startswith('/monsoon_pulse'):
            clean_path = clean_path[len('/monsoon_pulse'):]
        if clean_path == '' or clean_path == '/':
            clean_path = '/index.html'
        
        target = DIST_DIR / clean_path.lstrip('/')
        if target.exists():
            return str(target)
        return str(DIST_DIR / "index.html")


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def capture():
    port = find_free_port()
    server = HTTPServer(('127.0.0.1', port), BaseUrlHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Local server started on port {port} serving {DIST_DIR} under /monsoon_pulse/")

    url = f"http://127.0.0.1:{port}/monsoon_pulse/"
    screenshot_file = ASSETS_DIR / "dashboard_screenshot.png"

    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--window-size=1600,1050",
        f"--screenshot={str(screenshot_file)}",
        "--virtual-time-budget=6000",
        url
    ]

    print("Capturing live dashboard screenshot via Edge headless...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    print(f"Edge process completed with code: {result.returncode}")

    server.shutdown()
    
    if screenshot_file.exists():
        print(f"Successfully captured authentic dashboard screenshot: {screenshot_file} ({screenshot_file.stat().st_size} bytes)")
    else:
        print("Warning: Screenshot file not generated.")


if __name__ == "__main__":
    capture()
