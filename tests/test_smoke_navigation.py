# tests/test_smoke_navigation.py
import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

BASE = os.getenv("BASE_URL", "https://hrai.com.tr")
KEY_PAGES = [
    "/",
    "/Service/Index/",
    "/WhatIsHrAi/Index/",
    "/Demo/Index",
    "/Contact/Index/"
]

@pytest.mark.smoke
def test_site_availability(driver):
    # check each key page can be loaded and has non-empty body
    for p in KEY_PAGES:
        url = (BASE.rstrip("/") + p) if p.startswith("/") else BASE + "/" + p
        driver.get(url)
        WebDriverWait(driver, 6).until(lambda d: d.execute_script("return document.readyState === 'complete'"))
        body = driver.find_element(By.TAG_NAME, "body").text
        assert len(body.strip()) > 0, f"Empty body for {url}"
