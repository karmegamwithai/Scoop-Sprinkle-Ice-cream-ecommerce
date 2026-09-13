from django.contrib import messages
from django.shortcuts import render, redirect

from . import services
from .forms import RegisterForm, LoginForm, ProfileForm


def register_view(request):
    if request.session.get("user_id"):
        return redirect("home:home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user, error = services.register_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
            )
            if error:
                messages.error(request, error)
            else:
                services.login_session(request, user)
                messages.success(request, f"Welcome, {user['username']}! Your account was created.")
                return redirect("home:home")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.session.get("user_id"):
        return redirect("home:home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = services.authenticate_user(
                form.cleaned_data["username"], form.cleaned_data["password"]
            )
            if user:
                services.login_session(request, user)
                messages.success(request, f"Welcome back, {user['username']}!")
                next_url = request.GET.get("next") or "home:home"
                return redirect(next_url)
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    services.logout_session(request)
    messages.info(request, "You have been logged out.")
    return redirect("home:home")


@services.login_required
def profile_view(request):
    user = services.get_current_user(request)

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            services.update_profile(
                user["id"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
            )
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(initial={
            "email": user.get("email"),
            "phone": user.get("phone"),
            "address": user.get("address"),
        })

    return render(request, "accounts/profile.html", {"form": form, "user": user})
