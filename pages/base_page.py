# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)

    def find(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def find_visible(self, by, locator):
        return self.wait.until(EC.visibility_of_element_located((by, locator)))

    def click(self, el):
        from selenium.webdriver.remote.webelement import WebElement
        if isinstance(el, tuple):
            e = self.find_visible(*el)
            try:
                e.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", e)
        elif isinstance(el, WebElement):
            try:
                el.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", el)
        else:
            raise TypeError("Unsupported element for click")

    def send_keys(self, el, value):
        from selenium.webdriver.remote.webelement import WebElement
        if isinstance(el, tuple):
            e = self.find_visible(*el)
            e.clear()
            e.send_keys(value)
        elif isinstance(el, WebElement):
            el.clear()
            el.send_keys(value)
        else:
            raise TypeError("Unsupported element for send_keys")
