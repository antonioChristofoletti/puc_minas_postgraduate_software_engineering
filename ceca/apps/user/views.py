from apps.user.models import CustomUser
from apps.user.utils import redirect_not_auth_user
from django.contrib import auth, messages
from django.shortcuts import render, redirect


def login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method != "POST":
        return render(request, "user/login.html")
    
    form: dict = request.POST.dict()

    email: str = form.get("txt_email", "").strip()
    password: str = form.get("txt_password", "").strip()

    if not email:
        messages.error(request, "E-mail is invalid.")
        return redirect("login")

    if not password:
        messages.error(request, "Password is invalid.")
        return redirect("login")

    user: CustomUser = auth.authenticate(request, username=email, password=password)

    if user:
        auth.login(request, user)
        return redirect("index")

    messages.error(request, "E-mail or password not found.")
    return redirect("login")


def signout(request):
    redirection = redirect_not_auth_user(request)
    if redirection:
        return redirection

    auth.logout(request)
    messages.success(request, 'User signed out successfully')
    return redirect('login')
