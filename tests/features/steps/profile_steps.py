from behave import when, then
from selenium.webdriver.common.by import By

from tests.pages.profile_page import ProfilePage



@when('I navigate to the profile page')
def step_when_navigate_to_profile(context):
    context.profile_page.navigate_to_profile()

@then('I should see my name, role, and email')
def step_then_verify_profile_info(context):
    name, role, email = context.profile_page.verify_profile_info()
    assert name, "Name not displayed"
    assert role == "ACADI", "Role not displayed correctly"
    assert email == "1000612135@u.icesi.edu.co", "Email not displayed correctly"

@then('I can click the "Edit Profile" button to go to the edit page')
def step_then_click_edit_profile(context):
    context.profile_page.click_edit_profile()
    assert context.driver.current_url == f"{context.base_url}/dashboard/profile/edit/", "Did not redirect to edit page"

@when('I navigate to the profile edit page')
def step_when_navigate_to_edit_page(context):
    context.profile_page.navigate_to_profile()
    context.profile_page.click_edit_profile()

@when('I upload a valid image and save changes')
def step_when_upload_image(context):
    image_path = "tests/resources/test_image.jpg"
    context.profile_page.upload_image(image_path)
    context.profile_page.save_changes()

@then('I should see a success message')
def step_then_verify_success_message(context):
    assert context.profile_page.verify_success_message(), "Success message not displayed"

@then('my profile should show the updated image')
def step_then_verify_image_updated(context):
    context.profile_page.navigate_to_profile()
    assert context.profile_page.verify_image_updated(), "Image not updated"