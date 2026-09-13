from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.dashboard_login, name="login"),
    path("logout/", views.dashboard_logout, name="logout"),
    path("", views.dashboard_home, name="home"),

    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_add, name="product_add"),
    path("products/<str:product_id>/edit/", views.product_edit, name="product_edit"),
    path("products/<str:product_id>/delete/", views.product_delete, name="product_delete"),

    path("users/", views.user_list, name="user_list"),

    path("orders/", views.order_list, name="order_list"),
    path("orders/<str:order_id>/status/", views.order_update_status, name="order_update_status"),
]
