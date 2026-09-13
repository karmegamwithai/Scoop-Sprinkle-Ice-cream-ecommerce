"""
apps/accounts/services.py
Handles all customer-account logic against the "Users" Google Sheet,
plus session-based login helpers (since we are NOT using Django's auth
User model / SQL database for shop accounts).
"""
from functools import wraps

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect
from django.contrib import messages

from services import supabase_client as db

TABLE = settings.TABLE_USERS


def get_user_by_username(username):
    rows = db.get_rows_by_field(TABLE, "username", username)
    return rows[0] if rows else None


def get_user_by_email(email):
    rows = db.get_rows_by_field(TABLE, "email", email)
    return rows[0] if rows else None


def get_user_by_id(user_id):
    return db.get_row_by_id(TABLE, user_id)


def register_user(username, email, password, phone="", address=""):
    if get_user_by_username(username):
        return None, "Username already taken."
    if get_user_by_email(email):
        return None, "Email already registered."

    user = db.insert_row(TABLE, {
        "username": username,
        "email": email,
        "password": make_password(password),
        "phone": phone,
        "address": address,
        "created_at": db.now_str(),
    })
    return user, None


def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user and check_password(password, user.get("password", "")):
        return user
    return None


def update_profile(user_id, **fields):
    return db.update_row(TABLE, user_id, fields)


# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------
def login_session(request, user):
    request.session["user_id"] = user["id"]
    request.session["username"] = user["username"]


def logout_session(request):
    request.session.pop("user_id", None)
    request.session.pop("username", None)


def get_current_user(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return get_user_by_id(user_id)


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            messages.warning(request, "Please log in to continue.")
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapper


def session_user_context(request):
    """Template context processor: exposes `current_user` everywhere."""
    return {"current_user": get_current_user(request)}
