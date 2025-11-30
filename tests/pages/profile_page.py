from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.base_page import BasePage
import os

class ProfilePage(BasePage):
    NAME = (By.CLASS_NAME, "profile-name")
    ROLE = (By.CLASS_NAME, "profile-role")
    EMAIL = (By.CLASS_NAME, "profile-email")
    EDIT_PROFILE_BUTTON = (By.XPATH, "//a[@class='btn btn-primary btn-lg' and contains(text(), 'Edit Profile')]")
    PROFILE_IMAGE = (By.CLASS_NAME, "profile-image")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "alert-success")
    IMAGE_UPLOAD = (By.ID, "profile_picture")
    SAVE_CHANGES_BUTTON = (By.ID, "triggerModal")
    MODAL_CONFIRM_BUTTON = (By.ID, "submitReport")
    PROFILE_LINK = (By.XPATH, "//a[@href='/dashboard/profile/']")

    def navigate_to_profile(self):
        self.click(*self.PROFILE_LINK)

    def verify_profile_info(self):
        name = self.get_text(*self.NAME)
        role = self.get_text(*self.ROLE)
        email = self.get_text(*self.EMAIL)
        return name, role, email

    def click_edit_profile(self):
        self.click(*self.EDIT_PROFILE_BUTTON)

    def upload_image(self, image_path):
        absolute_path = os.path.abspath(image_path)
        self.enter_text(*self.IMAGE_UPLOAD, absolute_path)

    def save_changes(self):
        self.click(*self.SAVE_CHANGES_BUTTON)
        self.click(*self.MODAL_CONFIRM_BUTTON)

    def verify_image_updated(self):
        image = self.wait_for_element(*self.PROFILE_IMAGE)
        default_image = "https://www.pngitem.com/pimgs/m/150-1503945_transparent-user-png-default-user-image-png-png.png"
        return image.get_attribute("src") != default_image

    def verify_success_message(self):
        try:

            message = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            ).text
            return "Foto de perfil actualizada correctamente" in message
        except:
            return False