from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

url = "https://www.google.com/"

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Path to your ChromeDriver
# ...existing code...
service = Service(r"C:\VickyJD\Tools\chromedriver-win64\chromedriver-win64\chromedriver.exe")
# ...existing code...

# Launch browser
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url)

# Optional: wait for page to load
time.sleep(5)

# Optional: take screenshot
driver.save_screenshot("nifty_chart.png")

# Keep browser open or close it
# driver.quit()