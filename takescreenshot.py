import subprocess
import time
import pyautogui
import os
import sys

# Path to Chrome executable
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Target URL
url = "https://in.tradingview.com/chart/QSEqPD5h/"

# ⏩ Launch Chrome with default profile
subprocess.Popen([
    chrome_path,
    "--new-window",
    url 
])

# ⏳ Wait for page to load
time.sleep(10)  # Adjust if needed

# 📸 Take screenshot
screenshot_path = os.path.join(os.getcwd(), "tradingview_chart.png")
pyautogui.screenshot(screenshot_path)
print(screenshot_path)

# 🛑 Close Chrome window (Alt + F4 shortcut)
pyautogui.hotkey("alt", "f4")
sys.exit(0) 