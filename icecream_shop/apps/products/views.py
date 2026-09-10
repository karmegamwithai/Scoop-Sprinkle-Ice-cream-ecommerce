from django.shortcuts import render, get_object_or_404
from django.http import Http404

from . import services


def product_list(request):
    category = request.GET.get("category") or None
    search = request.GET.get("q") or None

    products = services.get_all_products(category=category, search=search)
    categories = services.get_categories()

    context = {
        "products": products,
        "categories": categories,
        "selected_category": category,
        "search_query": search or "",
    }
    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    product = services.get_product_by_id(product_id)
    if not product:
        raise Http404("Product not found")
    return render(request, "products/product_detail.html", {"product": product})
