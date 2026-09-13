"""
apps/cart/services.py
The shopping cart lives entirely in the Django session as
{ "<product_id>": <quantity>, ... } — no Google Sheet needed for it.
"""
from apps.products import services as product_services

CART_SESSION_KEY = "cart"


def _get_raw_cart(request):
    return request.session.setdefault(CART_SESSION_KEY, {})


def add_to_cart(request, product_id, quantity=1):
    cart = _get_raw_cart(request)
    product_id = str(product_id)
    cart[product_id] = cart.get(product_id, 0) + int(quantity)
    request.session.modified = True


def update_quantity(request, product_id, quantity):
    cart = _get_raw_cart(request)
    product_id = str(product_id)
    quantity = int(quantity)
    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = quantity
    request.session.modified = True


def remove_from_cart(request, product_id):
    cart = _get_raw_cart(request)
    cart.pop(str(product_id), None)
    request.session.modified = True


def clear_cart(request):
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True


def get_cart_items(request):
    """Returns a list of dicts: product info + quantity + subtotal."""
    cart = _get_raw_cart(request)
    items = []
    for product_id, qty in cart.items():
        product = product_services.get_product_by_id(product_id)
        if not product:
            continue
        price = float(product.get("price") or 0)
        items.append({
            "product": product,
            "quantity": qty,
            "subtotal": round(price * qty, 2),
        })
    return items


def get_cart_total(request):
    return round(sum(item["subtotal"] for item in get_cart_items(request)), 2)


def get_cart_count(request):
    cart = _get_raw_cart(request)
    return sum(cart.values())


def cart_context(request):
    """Template context processor: exposes `cart_count` on every page."""
    try:
        return {"cart_count": get_cart_count(request)}
    except Exception:
        return {"cart_count": 0}
