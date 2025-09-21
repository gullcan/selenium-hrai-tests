# tests/test_login_page.py
import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

BASE = os.getenv("BASE_URL", "https://hrai.com.tr")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def open_login(driver):
    driver.get(f"{BASE}/Login/Index/")
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState === 'complete'"))

@pytest.mark.auth
def test_login_success(driver):
    open_login(driver)
    driver.find_element(By.ID, "Username").send_keys(USERNAME)
    driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    # Başarılı giriş genelde private dashboard'e yönlendirir -> calendar id'si olabilir
    WebDriverWait(driver, 8).until(lambda d: ("Calendar/Index" not in d.current_url) or ("calendar" in d.page_source.lower() or "dashboard" in d.page_source.lower()))
    assert ("Login/Index" not in driver.current_url) or ("calendar" in driver.page_source.lower() or "dashboard" in driver.page_source.lower())

@pytest.mark.auth
def test_login_invalid(driver):
    open_login(driver)
    driver.find_element(By.ID, "Username").send_keys("baduser")
    driver.find_element(By.ID, "passwordField").send_keys("badpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    # Eğer başarısız giriyorsa genelde sayfada kalırsın; ya da error mesajı çıkar
    assert "Login/Index" in driver.current_url or ("invalid" in driver.page_source.lower() or "hata" in driver.page_source.lower())

@pytest.mark.auth
def test_logout(driver):
    # login first
    open_login(driver)
    driver.find_element(By.ID, "Username").send_keys(USERNAME)
    driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 8).until(lambda d: ("Login/Index" not in d.current_url))
    # attempt logout by submitting logoutForm via JS (sağlam bir fallback)
    driver.execute_script("""
        const f = document.querySelector('form#logoutForm');
        if (f) { f.submit(); return true; } else { return false; }
    """)
    # wait for redirect to login
    WebDriverWait(driver, 8).until(lambda d: "Login/Index" in d.current_url or "login" in d.title.lower())
    assert "Login/Index" in driver.current_url or "login" in driver.title.lower()
