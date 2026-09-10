"""
apps/dashboard/services.py
Admin authentication (checked against settings.ADMIN_USERNAME/PASSWORD)
plus dashboard summary stats pulled from the Google Sheets.
"""
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

from apps.products import services as product_services
from apps.orders import services as order_services
from apps.accounts import services as account_services


def authenticate_admin(username, password):
    return username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD


def login_session(request):
    request.session["is_admin"] = True
    request.session["admin_username"] = settings.ADMIN_USERNAME


def logout_session(request):
    request.session.pop("is_admin", None)
    request.session.pop("admin_username", None)


def is_admin_logged_in(request):
    return bool(request.session.get("is_admin"))


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_admin_logged_in(request):
            messages.warning(request, "Please log in to the dashboard.")
            return redirect("dashboard:login")
        return view_func(request, *args, **kwargs)
    return wrapper


def get_dashboard_stats():
    products = product_services.get_all_products()
    orders = order_services.get_all_orders()
    from services import supabase_client as db
    users = db.get_all_rows(settings.TABLE_USERS)

    total_revenue = round(sum(float(o.get("total_amount") or 0) for o in orders), 2)

    return {
        "product_count": len(products),
        "order_count": len(orders),
        "user_count": len(users),
        "total_revenue": total_revenue,
        "recent_orders": orders[:5],
        "low_stock": [p for p in products if int(p.get("stock") or 0) <= 5],
    }

