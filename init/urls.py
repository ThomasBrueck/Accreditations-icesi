from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home-view'),
    path('register', views.RegisterUserView.as_view(), name='register-user'),
    path('validate-email/<slug:action>/', views.VerifyEmailView.as_view(), name='verify-email'),  # Change ValidateEmailView to VerifyEmailView
    path('login/', views.LoginView.as_view(), name='login-user'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    
    
]