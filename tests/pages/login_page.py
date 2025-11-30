from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "id_username")
    PASSWORD_FIELD = (By.ID, "id_password")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Log in']")
    ERROR_MESSAGE = (By.CLASS_NAME, "error")

    def login(self, username, password):
        self.enter_text(*self.USERNAME_FIELD, username)
        self.enter_text(*self.PASSWORD_FIELD, password)
        self.click(*self.LOGIN_BUTTON)
        # Esperar redirección al dashboard
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard/")
        )

    def get_error_message(self):
        try:
            return self.get_text(*self.ERROR_MESSAGE)
        except:
            return ""