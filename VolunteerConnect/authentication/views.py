



from .forms import RegisterForm

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def home(request):
    return render(request, 'home.html')  # Render home.html


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("authentication:home")  # Update this redirect if needed
        else:
            print(form.errors)  # Debugging: Print errors in console
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})


def custom_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("authentication:home")  # Update this redirect if needed
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "auth/login.html")


def custom_logout(request):
    logout(request)
    return redirect("authentication:home")



