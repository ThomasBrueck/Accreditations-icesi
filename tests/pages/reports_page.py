from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.base_page import BasePage

class ReportsPage(BasePage):
    REPORTS_LINK = (By.XPATH, "//a[@href='/dashboard/reports/']")
    SEARCH_BAR = (By.ID, "search-bar")
    FILTER_BUTTON = (By.LINK_TEXT, "Buscar")
    STATUS_FILTER = (By.ID, "estado")
    APPLY_FILTER_BUTTON = (By.ID, "apply-filter")
    REPORT_ITEM = (By.CLASS_NAME, "report-item")
    REPORT_TITLE = (By.CLASS_NAME, "report-title")
    REPORT_STATUS = (By.CLASS_NAME, "report-status")
    FILTER_TAGS = (By.CLASS_NAME, "filter-bar")

    def navigate_to_reports(self):
        self.click(*self.REPORTS_LINK)
        WebDriverWait(self.driver, 5).until(
            EC.url_contains("/dashboard/reports/")
        )

    def apply_filter(self, search_term, status):
        self.enter_text(*self.SEARCH_BAR, search_term)
        self.driver.find_element(*self.SEARCH_BAR).send_keys(self.driver.Keys.ENTER)
        self.click(*self.FILTER_BUTTON)
        select = self.driver.Select(self.driver.find_element(*self.STATUS_FILTER))
        select.select_by_value(status)
        self.click(*self.APPLY_FILTER_BUTTON)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.REPORT_ITEM)
        )

    def get_reports(self):
        reports = []
        try:
            report_elements = self.driver.find_elements(*self.REPORT_ITEM)
            for element in report_elements:
                title = element.find_element(*self.REPORT_TITLE).text
                status = element.find_element(*self.REPORT_STATUS).text
                reports.append({"title": title, "status": status})
        except:
            pass
        return reports

    def verify_filter_tags(self, search_term, status):
        try:
            tags = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.FILTER_TAGS)
            ).text
            return search_term in tags and status in tags
        except:
            self.driver.save_screenshot("filter_tags_failure.png")
            return False