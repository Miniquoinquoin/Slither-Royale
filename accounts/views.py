
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from accounts.forms import SignUpForm


def register(request):
    form = SignUpForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")

    return render(request, "accounts/register.html", {"form": form})

def login(request):
    form = AuthenticationForm(request,data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_login(request,form.get_user())
        return redirect("game")

    return render(request, "registration/login.html", {"form": form})
