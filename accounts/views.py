
from django.shortcuts import redirect, render

from accounts.forms import SignUpForm


def register(request):
    form = SignUpForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")

    return render(request, "accounts/register.html", {"form": form})
