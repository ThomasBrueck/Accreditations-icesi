from behave import given
from tests.pages.login_page import LoginPage
from tests.pages.profile_page import ProfilePage
from tests.pages.comments_page import CommentsPage

@given('I am logged in as an authenticated user')
def step_given_logged_in(context):
    context.driver.get(f"{context.base_url}/login/")
    login_page = LoginPage(context.driver)
    login_page.login("1000612135@u.icesi.edu.co", "prueba1234*")
    expected_url = f"{context.base_url}/dashboard/admin-dashboard/"
    current_url = context.driver.current_url
    assert current_url == expected_url, f"Login failed, expected {expected_url}, got {current_url}"
    # Inicializar la página según el contexto
    if hasattr(context, 'feature') and 'Comments Management' in context.feature.name:
        context.comments_page = CommentsPage(context.driver)
    else:
        context.profile_page = ProfilePage(context.driver)

@given('I am logged in as a different authenticated user')
def step_given_different_user_logged_in(context):
    context.driver.get(f"{context.base_url}/login/")
    login_page = LoginPage(context.driver)
    login_page.login("1109920889@u.icesi.edu.co", "qwerty1.")
    expected_url = f"{context.base_url}/dashboard/admin-dashboard/"
    current_url = context.driver.current_url
    assert current_url == expected_url, f"Login failed, expected {expected_url}, got {current_url}"
    context.comments_page = CommentsPage(context.driver)