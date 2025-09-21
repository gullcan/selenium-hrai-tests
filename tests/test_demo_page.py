# tests/test_demo_page.py
import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = os.getenv("BASE_URL", "https://hrai.com.tr")

def open_demo(driver):
    driver.get(f"{BASE}/Demo/Index")
    WebDriverWait(driver, 5).until(lambda d: d.execute_script("return document.readyState === 'complete'"))

@pytest.mark.forms
def test_demo_form_empty(driver):
    open_demo(driver)
    current = driver.current_url
    # submit without filling -> browser should block (still same URL)
    btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    btn.click()
    time.sleep(0.5)
    assert driver.current_url == current, "Boş form gönderildiğinde sayfa değişmemeli (tarayıcı doğrulaması)."

@pytest.mark.forms
def test_demo_form_invalid_email(driver):
    open_demo(driver)
    driver.find_element(By.NAME, "fullName").send_keys("Test User")
    driver.find_element(By.NAME, "email").send_keys("not-an-email")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(0.5)
    # invalid email usually prevented by browser -> still same URL and no redirect
    assert "/Demo/Start" not in driver.current_url, "Geçersiz email ile redirect olmamalı."
    # Another sanity check: the email input validity
    validity = driver.execute_script("return document.querySelector('input[name=email]').validity.valid")
    assert validity is False, "Email input tarayıcı validasyonuna takılmalı."

@pytest.mark.forms
def test_demo_form_valid(driver):
    open_demo(driver)
    full = "Automation Test"
    email = os.getenv("USERNAME") + "@example.com" if os.getenv("USERNAME") else f"test+{int(time.time())}@example.com"
    driver.find_element(By.NAME, "fullName").clear()
    driver.find_element(By.NAME, "fullName").send_keys(full)
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Bekle: ya URL /Demo/Start olur ya da sayfada success/thank kelimeleri görünür
    WebDriverWait(driver, 8).until(
        lambda d: ("/Demo/Start" in d.current_url) or
                  ("thank" in d.page_source.lower()) or
                  ("success" in d.page_source.lower())
    )
    assert ("/Demo/Start" in driver.current_url) or ("thank" in driver.page_source.lower()) or ("success" in driver.page_source.lower())
