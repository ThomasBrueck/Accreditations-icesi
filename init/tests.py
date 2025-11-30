from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import RoleModel, VerificationCodeModel
from django.contrib.auth.models import AnonymousUser
from unittest.mock import patch
from django.core.mail import send_mail
from .utils import sendEmailCode


class HomeViewTest(TestCase):
    def test_home_view_get(self):
        response = self.client.get(reverse('home-view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'init/home.html')

class RegisterUserViewTest(TestCase):
    def setUp(self):
        RoleModel.objects.all().delete()

        self.role = RoleModel.objects.create(name="common")
        self.client = Client()

    def test_register_user_valid_data(self):
        response = self.client.post(reverse('register-user'), {
            'username': 'testuser',
            'email': 'test@u.icesi.edu.co',
            'password1': 'password@123',
            'password2': 'password@123',
            'role': self.role.id,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(email='test@u.icesi.edu.co').exists())
        
        self.assertRedirects(response, reverse('verify-email', kwargs={'action': 'register'}))

    def test_register_user_invalid_email(self):
        response = self.client.post(reverse('register-user'), {
            'username': 'testuser',
            'email': 'test@gmail.com', 
            'password1': 'password@123',
            'password2': 'password@123',
            'role': self.role.id,
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El correo no es institucional")

    def test_register_user_existing_email(self):
        get_user_model().objects.create_user(
            username='test@u.icesi.edu.co', 
            email='test@u.icesi.edu.co', 
            password='password@123', 
            role=self.role
        )
        
        response = self.client.post(reverse('register-user'), {
            'username': 'testuser2',
            'email': 'test@u.icesi.edu.co',
            'password1': 'password@123',
            'password2': 'password@123',
            'role': self.role.id,
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User with this Email already exists")

    def test_register_user_get(self):
        response = self.client.get(reverse('register-user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'init/register.html')
        self.assertIn('form', response.context)

    def test_register_user_empty_email(self):
        response = self.client.post(reverse('register-user'), {
            'username': 'testuser',
            'email': '',
            'password1': 'password@123',
            'password2': 'password@123',
            'role': self.role.id,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")

    def test_register_user_short_password(self):
        response = self.client.post(reverse('register-user'), {
            'username': 'testuser',
            'email': 'test@u.icesi.edu.co',
            'password1': '123',
            'password2': '123',
            'role': self.role.id,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This password is too short")

    def test_register_user_non_institutional_email(self):
        response = self.client.post(reverse('register-user'), {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password1': 'password@123',
            'password2': 'password@123',
            'role': self.role.id,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El correo no es institucional")

class VerifyEmailViewTest(TestCase):
    def setUp(self):
        RoleModel.objects.all().delete()

        self.role = RoleModel.objects.create(name="common")
        
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@u.icesi.edu.co',
            password='password@123',
            role=self.role
        )
       
        self.code = "123456"
        self.verification = VerificationCodeModel.objects.create(
            user=self.user,
            code=self.code
        )

    def test_verify_email_get(self):
        response = self.client.get(reverse('verify-email', kwargs={'action': 'register'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'init/validate_email.html')
        self.assertIn('form', response.context)
        self.assertIn('action', response.context)
        self.assertEqual(response.context['action'], 'register')

    def test_verify_email_post_valid_code_register(self):
        response = self.client.post(
            reverse('verify-email', kwargs={'action': 'register'}),
            {'code': self.code}
        )
        
        self.user.refresh_from_db()
        
        self.assertTrue(self.user.is_verified_code)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home-view'))
        
        self.assertEqual(VerificationCodeModel.objects.filter(code=self.code).count(), 0)

    def test_verify_email_post_invalid_code(self):
        response = self.client.post(
            reverse('verify-email', kwargs={'action': 'register'}),
            {'code': '000000'}
        )
        
        self.user.refresh_from_db()
        
        self.assertFalse(self.user.is_verified_code)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The code is wrong")

    def test_verify_email_post_valid_code_reset(self):
        session = self.client.session
        session["reset_email"] = self.user.email
        session.save()

        response = self.client.post(
            reverse('verify-email', kwargs={'action': 'reset'}),
            {'code': self.code}
        )

        self.assertRedirects(response, reverse('reset-password'), fetch_redirect_response=False)


    def test_verify_email_post_empty_code(self):
        response = self.client.post(
            reverse('verify-email', kwargs={'action': 'register'}),
            {'code': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")


class LoginViewTest(TestCase):
    def setUp(self):
        RoleModel.objects.all().delete()

        self.role = RoleModel.objects.create(name="common")
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@u.icesi.edu.co',
            password='password@123',
            role=self.role,
            is_verified_code=True
        )

    def test_login_view_get(self):
        response = self.client.get(reverse('login-user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'init/login.html')

    def test_login_valid_credentials(self):
        response = self.client.post(reverse('login-user'), {
            'username': 'test@u.icesi.edu.co',
            'password': 'password@123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('verify-email', kwargs={'action': 'login'}))

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login-user'), {
            'username': 'wrong@u.icesi.edu.co',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct email and password")

    def test_login_unverified_user(self):
        unverified_user = get_user_model().objects.create_user(
            username='unverifieduser',
            email='unverified@u.icesi.edu.co',
            password='password@123',
            role=self.role,
            is_verified_code=False
        )
            
        response = self.client.post(reverse('login-user'), {
            'username': 'unverified@u.icesi.edu.co',
            'password': 'password@123'
        })
            
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('verify-email', kwargs={'action': 'login'}))
        self.assertTrue(VerificationCodeModel.objects.filter(user=unverified_user).exists())

    def test_login_view_redirects_unverified_user(self):
        self.user.is_verified_code = False
        self.user.save()

        response = self.client.post(reverse('login-user'), {
            'username': self.user.email,
            'password': 'password@123'
        })

        self.assertRedirects(response, reverse('verify-email', kwargs={'action': 'login'}))



class ForgotPasswordViewTest(TestCase):
    def setUp(self):
        RoleModel.objects.all().delete()

        self.role = RoleModel.objects.create(name="common")
        self.user = get_user_model().objects.create_user(
            username='forgotuser',
            email='forgot@u.icesi.edu.co',
            password='password@123',
            role=self.role
        )

    def test_forgot_password_get(self):
        response = self.client.get(reverse('forgot-password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'init/forgot-password.html')

    def test_forgot_password_post_valid_email(self):
        response = self.client.post(reverse('forgot-password'), {
            'email': 'forgot@u.icesi.edu.co'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('verify-email', kwargs={'action': 'reset'}))
        self.assertEqual(self.client.session["reset_email"], 'forgot@u.icesi.edu.co')

    def test_forgot_password_post_invalid_email(self):
        response = self.client.post(reverse('forgot-password'), {
            'email': 'nonexistent@u.icesi.edu.co'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email doesn")
        self.assertContains(response, "exists")

    def test_forgot_password_empty_email(self):
        response = self.client.post(reverse('forgot-password'), {
            'email': '', 
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")

    def test_forgot_password_post_nonexistent_email(self):
        response = self.client.post(reverse('forgot-password'), {
            'email': 'nonexistent@u.icesi.edu.co'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email doesn")
        self.assertContains(response, "exists")


class ResetPasswordViewTest(TestCase):
    def setUp(self):
        RoleModel.objects.all().delete()

        self.role = RoleModel.objects.create(name="common")
        self.user = get_user_model().objects.create_user(
            username='resetuser',
            email='reset@u.icesi.edu.co',
            password='password@123',
            role=self.role
        )
        session = self.client.session
        session["reset_email"] = 'reset@u.icesi.edu.co'
        session.save()

    def test_reset_password_get_with_session(self):
        response = self.client.get(reverse("reset-password"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "init/reset-password.html")

    def test_reset_password_get_without_session(self):
        client = Client()
        response = client.get(reverse('reset-password'))
        self.assertRedirects(response, reverse('forgot-password'))

    def test_reset_password_post_valid(self):
        response = self.client.post(reverse("reset-password"), {
            "password1": "NewPassword123!",
            "password2": "NewPassword123!"
        })
        self.assertRedirects(response, reverse("login-user"))

    def test_reset_password_post_mismatched_passwords(self):
        response = self.client.post(reverse("reset-password"), {
            "password1": "password123",
            "password2": "password1234"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "init/reset-password.html")
        self.assertContains(response, "The passwords are different")

    def test_reset_password_post_empty_password(self):
        response = self.client.post(reverse("reset-password"), {
            "password1": "",
            "password2": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "init/reset-password.html")
        self.assertContains(response, "This field is required")


    def test_reset_password_redirect_if_no_session(self):
        self.client.session.flush()  # Remove session data
        response = self.client.get(reverse('reset-password'))
        self.assertRedirects(response, reverse('forgot-password'))

    def test_reset_password_redirect_after_successful_reset(self):
        response = self.client.post(reverse('reset-password'), {
            'password1': 'NewPassword123!',
            'password2': 'NewPassword123!'
        })
        self.assertRedirects(response, reverse('login-user'))

    def test_reset_password_post_mismatched_passwords(self):
        session = self.client.session
        session["reset_email"] = "reset@u.icesi.edu.co"
        session.save()

        response = self.client.post(reverse("reset-password"), {
            "password1": "NewPassword123!",
            "password2": "DifferentPassword456!"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The passwords are different")

    
class SendEmailCodeTest(TestCase):

    @patch('django.core.mail.send_mail')
    def test_send_email_code_failure(self, mock_send_mail):
        user = get_user_model().objects.create_user(
            username='testuser',
            email='test@u.icesi.edu.co',
            password='password@123'
        )
        code = "123456"

        mock_send_mail.side_effect = Exception("Mail server error")

        sendEmailCode(user, code)
