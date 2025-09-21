# pages/dashboard_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class DashboardPage(BasePage):
    URL = "https://hrai.com.tr/Calendar/Index/"
    CALENDAR = (By.ID, "calendar")
    def open_dashboard(self):
        self.open(self.URL)
    def loaded(self):
        return bool(self.find(*self.CALENDAR))
