# conftest.py
import os
import time
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

# .env yükle
load_dotenv()

# Base URL fixture
@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://hrai.com.tr")

# Kullanıcı bilgileri
@pytest.fixture(scope="session")
def credentials():
    return {
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    }

# Selenium driver fixture
@pytest.fixture
def driver():
    options = Options()
    # options.add_argument("--headless=new")  # CI/CD için açabilirsin
    options.add_argument("--window-size=1400,1000")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    yield driver
    driver.quit()

# Test hata aldığında screenshot al ve Allure raporuna ekle
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_dir = os.getenv("SCREENSHOT_DIR", "./screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            file_name = f"{item.name}_{int(time.time())}.png"
            path = os.path.join(screenshot_dir, file_name)

            driver.save_screenshot(path)
            allure.attach.file(
                path,
                name="Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
