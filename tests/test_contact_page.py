# tests/test_contact_page.py
import os
import time
import requests
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = os.getenv("BASE_URL", "https://hrai.com.tr")
DEMO_HEADERS = {"User-Agent": "security-scan/1.0"}

@pytest.mark.forms
def test_contact_form_missing_fields(driver):
    driver.get(f"{BASE}/Contact/Index/")
    WebDriverWait(driver, 5).until(lambda d: d.execute_script("return document.readyState === 'complete'"))
    submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit.click()
    time.sleep(0.5)
    # required inputs have attribute required -> browser should keep page (no redirect)
    assert driver.current_url.endswith("/Contact/Index/"), "Eksik alanlarda sayfa değişmemeli."

@pytest.mark.forms
def test_contact_form_invalid_email(driver):
    driver.get(f"{BASE}/Contact/Index/")
    driver.find_element(By.NAME, "Name").send_keys("Test User")
    driver.find_element(By.NAME, "Email").send_keys("invalid-email")
    # fill required other fields minimally
    driver.find_element(By.NAME, "MessageTitle").send_keys("Title")
    driver.find_element(By.NAME, "Message").send_keys("msg")
    # do not check consent to see browser behaviour for required checkbox
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(0.5)
    # tarayıcı-level email validation: still same page
    assert driver.current_url.endswith("/Contact/Index/")
    valid = driver.execute_script("return document.querySelector('input[name=Email]').validity.valid")
    assert valid is False

@pytest.mark.forms
def test_contact_form_valid(driver):
    driver.get(f"{BASE}/Contact/Index/")
    WebDriverWait(driver, 5).until(lambda d: d.execute_script("return document.readyState === 'complete'"))
    driver.find_element(By.NAME, "Name").send_keys("Auto Tester")
    email = os.getenv("USERNAME") + "@example.com" if os.getenv("USERNAME") else f"test+{int(time.time())}@example.com"
    driver.find_element(By.NAME, "Email").send_keys(email)
    # If phone input exists, skip or fill minimal
    try:
        phone = driver.find_element(By.ID, "intl-phone")
        phone.send_keys("5551234567")
    except:
        pass
    driver.find_element(By.NAME, "MessageTitle").send_keys("Automation Test")
    driver.find_element(By.NAME, "Message").send_keys("This is an automated contact message for test purposes.")
    # consent checkbox required -> check it
    consent = driver.find_element(By.ID, "consent")
    if not consent.is_selected():
        consent.click()
    # submit
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    # wait for either redirect away or success indicator
    WebDriverWait(driver, 8).until(lambda d: ("/Contact/Index" not in d.current_url) or ("thank" in d.page_source.lower()) or ("success" in d.page_source.lower()))
    assert ("/Contact/Index" not in driver.current_url) or ("thank" in driver.page_source.lower()) or ("success" in driver.page_source.lower())

@pytest.mark.forms
def test_contact_form_sql_injection():
    """
    Basit error-leakage kontrolü: contact endpoint'e kötü payload gönderip
    sunucunun hata mesajı döndürmediğini doğrularız.
    """
    session = requests.Session()
    session.headers.update(DEMO_HEADERS)
    try:
        r = session.get(f"{BASE}/Contact/Index/", timeout=8)
    except Exception as e:
        pytest.skip(f"GET failed: {e}")

    data = {
        "Name": "' OR '1'='1",
        "Email": "inject@example.com",
        "MessageTitle": "sqli",
        "Message": "'; DROP TABLE users; --",
        # CSRF token is present in page as hidden; but we can't easily extract without parsing.
        # This test is only for response body leakage when posting (may be blocked by WAF)
    }
    try:
        r2 = session.post(f"{BASE}/Contact/SendForm", data=data, timeout=10, allow_redirects=True)
    except Exception as e:
        pytest.skip(f"POST failed: {e}")

    body = r2.text.lower()
    suspicious = ["sql", "syntax", "exception", "bad query", "mysql", "odbc", "pdoexception", "sqlerror", "server error"]
    found = [k for k in suspicious if k in body]
    assert not found, f"Potential DB error leakage found: {found}"
