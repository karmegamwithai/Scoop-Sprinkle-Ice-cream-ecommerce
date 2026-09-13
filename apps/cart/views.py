from django.contrib import messages
from django.shortcuts import render, redirect

from . import services


def cart_view(request):
    items = services.get_cart_items(request)
    total = services.get_cart_total(request)
    return render(request, "cart/cart.html", {"items": items, "total": total})


def add_to_cart(request, product_id):
    quantity = request.POST.get("quantity", 1)
    services.add_to_cart(request, product_id, quantity)
    messages.success(request, "Added to cart 🍦")
    next_url = request.POST.get("next") or "products:list"
    return redirect(next_url)


def update_cart(request, product_id):
    quantity = request.POST.get("quantity", 1)
    services.update_quantity(request, product_id, quantity)
    return redirect("cart:view")


def remove_from_cart(request, product_id):
    services.remove_from_cart(request, product_id)
    messages.info(request, "Item removed from cart.")
    return redirect("cart:view")
