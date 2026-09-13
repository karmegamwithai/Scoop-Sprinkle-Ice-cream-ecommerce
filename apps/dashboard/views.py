from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect

from apps.products import services as product_services
from apps.products.forms import ProductForm
from apps.orders import services as order_services
from services import supabase_client as db

from . import services
from .forms import AdminLoginForm


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
def dashboard_login(request):
    if services.is_admin_logged_in(request):
        return redirect("dashboard:home")

    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            if services.authenticate_admin(
                form.cleaned_data["username"], form.cleaned_data["password"]
            ):
                services.login_session(request)
                return redirect("dashboard:home")
            messages.error(request, "Invalid admin credentials.")
    else:
        form = AdminLoginForm()

    return render(request, "dashboard/login.html", {"form": form})


def dashboard_logout(request):
    services.logout_session(request)
    return redirect("dashboard:login")


# ---------------------------------------------------------------------------
# Dashboard home
# ---------------------------------------------------------------------------
@services.admin_required
def dashboard_home(request):
    stats = services.get_dashboard_stats()
    return render(request, "dashboard/dashboard.html", {"stats": stats})


# ---------------------------------------------------------------------------
# Products CRUD
# ---------------------------------------------------------------------------
@services.admin_required
def product_list(request):
    products = product_services.get_all_products()
    return render(request, "dashboard/products/list.html", {"products": products})


@services.admin_required
def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product_services.create_product(**form.cleaned_data)
            messages.success(request, "Product added.")
            return redirect("dashboard:product_list")
    else:
        form = ProductForm()

    return render(request, "dashboard/products/add.html", {"form": form})


@services.admin_required
def product_edit(request, product_id):
    product = product_services.get_product_by_id(product_id)
    if not product:
        raise Http404("Product not found")

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product_services.update_product(product_id, **form.cleaned_data)
            messages.success(request, "Product updated.")
            return redirect("dashboard:product_list")
    else:
        form = ProductForm(initial=product)

    return render(request, "dashboard/products/edit.html", {"form": form, "product": product})


@services.admin_required
def product_delete(request, product_id):
    if request.method == "POST":
        product_services.delete_product(product_id)
        messages.success(request, "Product deleted.")
    return redirect("dashboard:product_list")


# ---------------------------------------------------------------------------
# Users (read-only)
# ---------------------------------------------------------------------------
@services.admin_required
def user_list(request):
    users = db.get_all_rows(settings.TABLE_USERS)
    return render(request, "dashboard/users/list.html", {"users": users})


# ---------------------------------------------------------------------------
# Orders
# ---------------------------------------------------------------------------
@services.admin_required
def order_list(request):
    orders = order_services.get_all_orders()
    return render(request, "dashboard/orders/list.html", {"orders": orders})


@services.admin_required
def order_update_status(request, order_id):
    if request.method == "POST":
        status = request.POST.get("status", "Pending")
        order_services.update_order_status(order_id, status)
        messages.success(request, f"Order #{order_id} marked as {status}.")
    return redirect("dashboard:order_list")
