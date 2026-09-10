from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from apps.accounts import services as account_services
from apps.cart import services as cart_services
from . import services
from .forms import CheckoutForm


@account_services.login_required
def checkout_view(request):
    user = account_services.get_current_user(request)
    items = cart_services.get_cart_items(request)
    total = cart_services.get_cart_total(request)

    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect("products:list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = services.create_order(
                user=user,
                cart_items=items,
                address=form.cleaned_data["address"],
                phone=form.cleaned_data["phone"],
            )
            cart_services.clear_cart(request)
            return redirect("orders:success", order_id=order["id"])
    else:
        form = CheckoutForm(initial={
            "address": user.get("address", ""),
            "phone": user.get("phone", ""),
        })

    return render(request, "orders/checkout.html", {
        "form": form, "items": items, "total": total,
    })


@account_services.login_required
def order_success_view(request, order_id):
    order = services.get_order_by_id(order_id)
    if not order:
        raise Http404("Order not found")
    return render(request, "orders/order_success.html", {"order": order})


@account_services.login_required
def orders_view(request):
    user = account_services.get_current_user(request)
    orders = services.get_orders_by_user(user["id"])
    return render(request, "orders/orders.html", {"orders": orders})
