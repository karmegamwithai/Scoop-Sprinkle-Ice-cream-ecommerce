from django.shortcuts import render
from apps.products import services as product_services


def home_view(request):
    products = product_services.get_all_products()
    featured = products[:6]
    return render(request, "home/home.html", {"featured_products": featured})
