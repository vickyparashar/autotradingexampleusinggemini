"""
Capture a TradingView screenshot using Chrome + pyautogui.

- Import as a module: from takescreenshot import capture
- Run as a script: python takescreenshot.py
"""

import os
import sys
import time
import pyautogui
import subprocess
from pathlib import Path
import psutil

# ------------------------------
# Defaults (used by CLI mode)
# ------------------------------
DEFAULT_CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DEFAULT_URL = "https://in.tradingview.com/chart/QSEqPD5h/"
DEFAULT_OUT = Path(os.getcwd()) / "tradingview_chart.png"

# Wait settings
INITIAL_LOAD_WAIT = 8   # base wait for browser to start
FULL_LOAD_EXTRA_WAIT = 5  # wait after page is considered 'loaded'

def _launch_chrome(url: str, chrome_path: str) -> subprocess.Popen:
    """Launch Chrome to a URL and return the process handle."""
    return subprocess.Popen(
        [chrome_path, "--new-window", url],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def _graceful_close():
    """Try to close the active window via Alt+F4."""
    try:
        pyautogui.click(100, 100)  # bring Chrome into focus
        time.sleep(0.5)
        pyautogui.hotkey("alt", "f4")
    except Exception as e:
        print(f"[takescreenshot] Alt+F4 close failed: {e}", file=sys.stderr)

def _kill_chrome_tree(proc: subprocess.Popen):
    """Kill the Chrome process and all its children."""
    try:
        parent = psutil.Process(proc.pid)
        for child in parent.children(recursive=True):
            child.terminate()
        parent.terminate()
    except psutil.NoSuchProcess:
        pass

def capture(
    url: str = DEFAULT_URL,
    out_path: Path = DEFAULT_OUT,
    chrome_path: str = DEFAULT_CHROME_PATH,
) -> Path:
    """
    Launch Chrome to the URL, wait for page to load, screenshot to out_path, and close the window.

    Returns the saved Path.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Launch Chrome
    proc = _launch_chrome(url, chrome_path)

    # 2. Wait for initial load
    time.sleep(INITIAL_LOAD_WAIT)

    # (Optional) — here we could integrate Selenium or pygetwindow to detect when page load is complete
    # For now, just add extra wait so TradingView fully renders
    time.sleep(FULL_LOAD_EXTRA_WAIT)

    # 3. Take screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save(out_path)

    # 4. Close Chrome
    _graceful_close()
    time.sleep(1)  # small buffer before kill

    # 5. Force kill to ensure clean exit
    _kill_chrome_tree(proc)

    return out_path

# ------------------------------
# CLI entry
# ------------------------------
if __name__ == "__main__":
    try:
        path = capture()
        print(str(path))
        sys.exit(0)
    except Exception as e:
        print(f"[takescreenshot] ERROR: {e}", file=sys.stderr)
        sys.exit(1)