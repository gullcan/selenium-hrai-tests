# utils/test_helpers.py
import os
import time

def save_screenshot(driver, name_prefix="fail"):
    name = f"{name_prefix}_{int(time.time())}.png"
    folder = os.getenv("SCREENSHOT_DIR", ".")
    path = os.path.join(folder, name)
    driver.save_screenshot(path)
    return path
