from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect("/")

@login_required
def protected_page(request):
    return render(request, "protected_page.html")

