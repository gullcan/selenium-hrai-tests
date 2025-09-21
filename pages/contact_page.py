from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ContactPage:
    URL = "/Contact/Index"

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url + self.URL)

    def fill_form(self, name, email, phone, company, title, message):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "name")))

        self.driver.find_element(By.ID, "name").send_keys(name)
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "intl-phone").send_keys(phone)
        self.driver.find_element(By.ID, "company").send_keys(company)
        self.driver.find_element(By.ID, "title").send_keys(title)
        self.driver.find_element(By.ID, "message").send_keys(message)
        self.driver.find_element(By.ID, "consent").click()

    def submit(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
