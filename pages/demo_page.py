from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DemoPage:
    URL = "/Demo/Index"

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url + self.URL)

    def fill_form(self, name, email):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "fullName"))
        )
        self.driver.find_element(By.ID, "fullName").send_keys(name)
        self.driver.find_element(By.ID, "email").send_keys(email)

    def submit(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
