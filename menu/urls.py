from django.urls import path

from menu.views import (
    ItemDetailView,
    ItemListView,
    OrderCheckoutView,
    OrderModifyView,
    OrderView,
)

app_name = "menu"

urlpatterns = [
    path("", ItemListView.as_view(), name="all"),
    path("item/<int:pk>", ItemDetailView.as_view(), name="item"),
    path("order/", OrderView.as_view(), name="order"),
    path(
        "item/<int:pk>/<str:action>",
        OrderModifyView.as_view(),
        name="order_modify",
    ),
    path("order/checkout", OrderCheckoutView.as_view(), name="order_checkout"),
]
