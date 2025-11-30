from django import forms
from .models import UserModel, VerificationCodeModel, RoleModel
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ["username", "email", "password1", "password2"]

class ValidateEmailForm(forms.ModelForm):

    class Meta:
        model = VerificationCodeModel
        fields = ["code"]

class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email")

class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label="New password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm new password")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("The passwords are different")
        
        return cleaned_data