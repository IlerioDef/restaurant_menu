from django.urls import path

from menu.views import (
    AddItemView,
    ItemDetailView,
    ItemListView,
    OrderCheckoutView,
    OrderView,
    RemoveItemView,
)

app_name = "menu"

urlpatterns = [
    path("", ItemListView.as_view(), name="all"),
    path("item/<int:pk>", ItemDetailView.as_view(), name="item"),
    path("order/", OrderView.as_view(), name="order"),
    path("add_item/<int:item_id>", AddItemView.as_view(), name="add_item"),
    path(
        "remove_item/<int:item_id>",
        RemoveItemView.as_view(),
        name="remove_item",
    ),
    path("order/checkout", OrderCheckoutView.as_view(), name="order_checkout"),
]
