import os
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from .forms import RegisterUserForm, ValidateEmailForm, LoginUserForm, ForgotPasswordForm, ResetPasswordForm
from .models import UserModel, VerificationCodeModel, RoleModel
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import random
from .utils import sendEmailCode
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

universities = [
    "@u.icesi.edu.co", # Common user
    "@icesi.edu.co" # Admin user / Acadi
]

class HomeView(View):
    
    def get(self, request):
        return render(request, "init/home.html")
    
class RegisterUserView(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, "init/register.html", {
            "form": form,
        })
    
    def post(self, request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            is_institutional = False
            for university_email in universities:
                if email.endswith(university_email):
                    is_institutional = True
                    break
        
            if not is_institutional:
                form.add_error("email", "El correo no es institucional")
                return render(request, "init/register.html", {
                    "form": form
                })

            if UserModel.objects.filter(email=email).exists():
                form.add_error("email", "Ese correo ya esta registrado")
                return render(request, "init/register.html", {
                    "form": form
                })
            
            user = form.save(commit=False)
            
            user.role = RoleModel.objects.get(name="common")
            user.save()
            code = str(random.randint(100000, 999999))

            VerificationCodeModel.objects.filter(user=user).delete()
            VerificationCodeModel.objects.create(user=user, code=code)
            sendEmailCode(user, code)

            return redirect("verify-email", action="register")

        return render(request, "init/register.html", {
            "form": form
        })
        


class VerifyEmailView(View):

    def get(self, request, action):
        form = ValidateEmailForm()
        return render(request, "init/validate_email.html", {
            "form": form,
            "action": action,
        })
    
    def post(self, request, action):
        form = ValidateEmailForm(request.POST)
        
        if form.is_valid():
            code = form.cleaned_data['code']

            verification = VerificationCodeModel.objects.filter(code=code).first()

            if verification:
                verification.user.is_verified_code = True
                verification.user.save()

                verification.delete()

                if action == 'register':
                    return redirect('home-view')
                
                elif action == 'login':
                    if verification.user.role.name == 'common':
                        return redirect('dashboard-user')
                    
                    elif verification.user.role.name == 'program director' or verification.user.role.name == 'acadi':
                        return redirect('dashboard-admin')
                    
                    else:
                        return redirect('home-view')
                    
                elif action == 'reset':
                    return redirect('reset-password')

        form.add_error("code", "The code is wrong")
        return render(request, "init/validate_email.html", {
            "form": form,
            "action": action,
        })


class LoginView(View):

    def get(self, request):
        form = LoginUserForm()
        
        return render(request, "init/login.html", {
            "form": form,
        })
    
    def post(self, request):
        form = LoginUserForm(request, data=request.POST)

        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=email, password=password)

            if user is not None:
                
                login(request, user)

                if os.getenv("TEST_MODE") == "True":
                    # Omitir verificación y redirigir según el rol
                    if user.role.name == 'common':
                        return redirect('dashboard-user')
                    elif user.role.name in ['program director', 'acadi']:
                        return redirect('dashboard-admin')
                    else:
                        return redirect('home-view')
                else:
                    # Lógica normal con verificación
                    code = str(random.randint(100000, 999999))
                    VerificationCodeModel.objects.filter(user=user).delete()
                    VerificationCodeModel.objects.create(user=user, code=code)
                    sendEmailCode(user, code)
                    return redirect("verify-email", action="login")
            
            else:

                form.add_error(None, "Invalid username or password")
                return render(request, "init/login.html", {
                    "form": form,
                })
        
        return render(request, "init/login.html", {
            "form": form,
        })
    
class ForgotPasswordView(View):
    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, "init/forgot-password.html", {
            "form": form
        })
    
    def post(self, request):
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            user = UserModel.objects.filter(email=email).first()

            if user:
                code = str(random.randint(100000, 999999))

                VerificationCodeModel.objects.filter(user=user).delete()
                VerificationCodeModel.objects.create(user=user, code=code)

                sendEmailCode(user, code)

                request.session["reset_email"] = email
                return redirect("verify-email", action="reset")
            
            form.add_error("email", "Email doesn't exists")
        return render(request, "init/forgot-password.html", {"form": form})


class ResetPasswordView(View):
    def get(self, request):
        email = request.session.get("reset_email")

        if not email:
            return redirect("forgot-password")
        
        form = ResetPasswordForm()
        return render(request, "init/reset-password.html", {
            "form": form,
            "email": email
        })

    def post(self, request):
        email = request.session.get("reset_email")

        if not email:
            return redirect("forgot-password")
        
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = UserModel.objects.filter(email=email).first()

            if user:
                user.set_password(form.cleaned_data['password1'])
                user.save()
                request.session.pop("reset_email", None)

                return redirect("login-user")
        
        return render(request, "init/reset-password.html", {
            "form": form,
            "email": email
        })

                


    


    

    
