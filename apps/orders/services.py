"""
apps/orders/services.py
CRUD helpers against the "orders" Supabase table.
Each order stores its line items in the `items` jsonb column,
e.g. [{"product_id": 3, "name": "Mango Tango", "price": 120, "quantity": 2}]
Supabase's client serializes/deserializes jsonb columns automatically, so
`items` arrives back as a native Python list — no manual json.loads needed.
"""
from django.conf import settings
from services import supabase_client as db
from apps.products import services as product_services

TABLE = settings.TABLE_ORDERS


def create_order(user, cart_items, address, phone):
    """
    cart_items: list of {"product": {...}, "quantity": int, "subtotal": float}
    """
    line_items = [{
        "product_id": item["product"]["id"],
        "name": item["product"]["name"],
        "price": float(item["product"]["price"]),
        "quantity": item["quantity"],
    } for item in cart_items]

    total = round(sum(i["subtotal"] for i in cart_items), 2)

    order = db.insert_row(TABLE, {
        "user_id": user["id"],
        "username": user["username"],
        "items": line_items,
        "total_amount": total,
        "address": address,
        "phone": phone,
        "status": "Pending",
        "created_at": db.now_str(),
    })

    for item in cart_items:
        product_services.decrement_stock(item["product"]["id"], item["quantity"])

    return order


def get_orders_by_user(user_id):
    orders = db.get_rows_by_field(TABLE, "user_id", user_id)
    for o in orders:
        o["items_parsed"] = o.get("items") or []
    return sorted(orders, key=lambda o: o.get("created_at", ""), reverse=True)


def get_all_orders():
    orders = db.get_all_rows(TABLE)
    for o in orders:
        o["items_parsed"] = o.get("items") or []
    return sorted(orders, key=lambda o: o.get("created_at", ""), reverse=True)


def get_order_by_id(order_id):
    order = db.get_row_by_id(TABLE, order_id)
    if order:
        order["items_parsed"] = order.get("items") or []
    return order


def update_order_status(order_id, status):
    return db.update_row(TABLE, order_id, {"status": status})
