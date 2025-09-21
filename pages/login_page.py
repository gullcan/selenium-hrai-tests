from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "/Login/Index"

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url + self.URL)

    def login(self, username, password):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "Username")))

        self.driver.find_element(By.ID, "Username").send_keys(username)
        self.driver.find_element(By.ID, "passwordField").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
