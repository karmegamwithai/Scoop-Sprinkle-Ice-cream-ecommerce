"""
apps/products/services.py
CRUD helpers against the "Products" Google Sheet.
"""
from django.conf import settings
from datetime import datetime
from decimal import Decimal
from services import supabase_client as db

TABLE = settings.TABLE_PRODUCTS


def get_all_products(category=None, search=None):
    products = db.get_all_rows(TABLE)
    if category:
        products = [p for p in products if str(p.get("category", "")).lower() == category.lower()]
    if search:
        s = search.lower()
        products = [p for p in products if s in str(p.get("name", "")).lower()
                    or s in str(p.get("flavor", "")).lower()]
    return products


def get_categories():
    products = db.get_all_rows(TABLE)
    return sorted({p.get("category") for p in products if p.get("category")})


def get_product_by_id(product_id):
    return db.get_row_by_id(TABLE, product_id)


def create_product(name, description, price, flavor, category, stock, image_url):
    return db.insert_row(TABLE, {
        "name": name,
        "description": description,
        "price": float(price),
        "flavor": flavor,
        "category": category,
        "stock": int(stock),
        "image_url": image_url,
        "created_at": datetime.now().isoformat(),
    })


def update_product(product_id, **fields):
    return db.update_row(TABLE, product_id, fields)


def delete_product(product_id):
    return db.delete_row(TABLE, product_id)


def decrement_stock(product_id, quantity):
    product = get_product_by_id(product_id)
    if not product:
        return None
    new_stock = max(0, int(product.get("stock", 0)) - int(quantity))
    return update_product(product_id, stock=new_stock)
