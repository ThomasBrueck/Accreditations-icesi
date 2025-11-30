from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 15  # Aumentar a 15 segundos para mayor robustez

    def wait_for_element(self, by, value):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    def wait_for_clickable(self, by, value):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def click(self, by, value):
        element = self.wait_for_clickable(by, value)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()
        except:
            # Fallback a clic con JavaScript
            self.driver.execute_script("arguments[0].click();", element)

    def enter_text(self, by, value, text):
        element = self.wait_for_element(by, value)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, value):
        element = self.wait_for_element(by, value)
        return element.text