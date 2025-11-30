from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.base_page import BasePage

class CommentsPage(BasePage):
    COMMENTS_LINK = (By.XPATH, "//a[@href='/dashboard/factors/1/comments/']")
    CREATE_COMMENT_LINK = (By.XPATH, "//a[@href='/dashboard/factors/1/comments/create/']")
    COMMENT_TITLE = (By.ID, "comment_title")
    COMMENT_CONTENT = (By.ID, "comment_content")
    SUBMIT_BUTTON = (By.ID, "submit_comment")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "alert-success")
    ERROR_MESSAGE = (By.XPATH, "//*[contains(@class, 'alert-danger') or contains(@class, 'error')]")
    COMMENT_ITEM = (By.CLASS_NAME, "comment-item")
    COMMENT_STATUS = (By.CLASS_NAME, "comment-status")
    EDIT_BUTTON = (By.CLASS_NAME, "edit-comment")
    DELETE_BUTTON = (By.CLASS_NAME, "delete-comment")
    APPROVE_BUTTON = (By.ID, "approve_button")
    DISAPPROVE_BUTTON = (By.ID, "disapprove_button")
    JUSTIFICATION_FIELD = (By.ID, "justification")
    JUSTIFICATION_TEXT = (By.CLASS_NAME, "justification-text")

    def navigate_to_comments_creation(self):
        self.click(*self.COMMENTS_LINK)
        self.click(*self.CREATE_COMMENT_LINK)
        WebDriverWait(self.driver, 5).until(
            EC.url_contains("/dashboard/factors/1/comments/create/")
        )

    def create_comment(self, title, content):
        self.enter_text(*self.COMMENT_TITLE, title)
        self.enter_text(*self.COMMENT_CONTENT, content)
        self.click(*self.SUBMIT_BUTTON)
        WebDriverWait(self.driver, 5).until(
            EC.url_contains("/dashboard/factors/1/comments/")
        )

    def get_last_comment_id(self):
        comments = self.get_comments()
        if comments:
            return comments[0]["id"]  # Último comentario es el primero en la lista
        return None

    def navigate_to_edit_comment(self, comment_id):
        self.driver.get(f"{self.base_url}/dashboard/factors/1/comments/edit/{comment_id}/")
        WebDriverWait(self.driver, 5).until(
            EC.url_contains(f"/dashboard/factors/1/comments/edit/{comment_id}/")
        )

    def update_comment(self, title, content):
        self.enter_text(*self.COMMENT_TITLE, title)
        self.enter_text(*self.COMMENT_CONTENT, content)
        self.click(*self.SUBMIT_BUTTON)
        WebDriverWait(self.driver, 5).until(
            EC.url_contains("/dashboard/factors/1/comments/")
        )

    def delete_comment(self, comment_id):
        self.driver.get(f"{self.base_url}/dashboard/factors/1/comments/")
        comment_element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@data-comment-id='{comment_id}']"))
        )
        comment_element.find_element(*self.DELETE_BUTTON).click()
        WebDriverWait(self.driver, 5).until(
            EC.url_contains("/dashboard/factors/1/comments/")
        )

    def attempt_delete_comment(self, comment_id):
        self.driver.get(f"{self.base_url}/dashboard/factors/1/comments/")
        try:
            comment_element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, f"//div[@data-comment-id='{comment_id}']"))
            )
            comment_element.find_element(*self.DELETE_BUTTON).click()
        except:
            pass  # Error esperado si el botón no está visible

    def navigate_to_review_page(self, comment_id):
        self.driver.get(f"{self.base_url}/comments/{comment_id}/review/")
        WebDriverWait(self.driver, 5).until(
            EC.url_contains(f"/comments/{comment_id}/review/")
        )

    def approve_comment(self):
        self.click(*self.APPROVE_BUTTON)
        WebDriverWait(self.driver, 5).until(
            EC.url_contains("/dashboard/factors/1/comments/")
        )

    def disapprove_comment(self, justification):
        self.enter_text(*self.JUSTIFICATION_FIELD, justification)
        self.click(*self.DISAPPROVE_BUTTON)
        WebDriverWait(self.driver, 5).until(
            EC.url_contains("/dashboard/factors/1/comments/")
        )

    def navigate_to_justification_page(self, comment_id):
        self.driver.get(f"{self.base_url}/comments/{comment_id}/justification/")
        WebDriverWait(self.driver, 5).until(
            EC.url_contains(f"/comments/{comment_id}/justification/")
        )

    def get_comments(self):
        comments = []
        try:
            self.driver.get(f"{self.base_url}/dashboard/factors/1/comments/")
            comment_elements = self.driver.find_elements(*self.COMMENT_ITEM)
            for element in comment_elements:
                title = element.find_element(By.CLASS_NAME, "comment-title").text
                status = element.find_element(*self.COMMENT_STATUS).text
                comment_id = element.get_attribute("data-comment-id")
                comments.append({"title": title, "status": status, "id": comment_id})
        except:
            pass
        return comments

    def verify_success_message(self, expected_message):
        try:
            message = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            ).text
            return expected_message in message
        except:
            self.driver.save_screenshot("success_message_failure.png")
            return False

    def verify_error_message(self, expected_message):
        try:
            message = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            ).text
            return expected_message in message
        except:
            self.driver.save_screenshot("error_message_failure.png")
            return False

    def verify_justification(self, expected_justification):
        try:
            justification = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.JUSTIFICATION_TEXT)
            ).text
            return expected_justification in justification
        except:
            self.driver.save_screenshot("justification_failure.png")
            return False