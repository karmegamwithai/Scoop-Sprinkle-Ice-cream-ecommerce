from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Django Admin
    path("django-admin/", admin.site.urls),

    # Home
    path("", include("apps.home.urls")),

    # Authentication
    path("accounts/", include("apps.accounts.urls")),

    # Products
    path("products/", include("apps.products.urls")),

    # Cart
    path("cart/", include("apps.cart.urls")),

    # Orders
    path("orders/", include("apps.orders.urls")),

    # Dashboard
    path("dashboard/", include("apps.dashboard.urls")),
]


# Serve static/media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )