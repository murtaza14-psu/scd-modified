from .forms import *

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



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

@login_required
def profile(request):
    user = request.user

    if user.role == 'volunteer':
        form = VolunteerProfileForm(request.POST or None, initial={
            'skills': user.volunteer_profile.skills,
            'interests': user.volunteer_profile.interests
        })

        if request.method == 'POST' and form.is_valid():
            user.volunteer_profile.skills = form.cleaned_data['skills']
            user.volunteer_profile.interests = form.cleaned_data['interests']
            user.volunteer_profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('authentication:profile')

        return render(request, 'profile/volunteer_profile.html', {'form': form})

    else:
        form = NGOProfileForm(request.POST or None, initial={
            'organization_name': user.ngo_profile.organization_name,
            'description': user.ngo_profile.description
        })

        if request.method == 'POST' and form.is_valid():
            user.ngo_profile.organization_name = form.cleaned_data['organization_name']
            user.ngo_profile.description = form.cleaned_data['description']
            user.ngo_profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('authentication:profile')

        return render(request, 'profile/ngo_profile.html', {'form': form})