import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from menu.models import Chef, Item, Order, OrderItem, Table


# Create your views here.
class ItemListView(View):
    template_name = "menu/item_list.html"

    def get(self, request, *args, **kwargs):
        _search = request.GET.get("search")
        if _search is not None and _search.strip():
            query = Q(name__icontains=_search) | Q(
                description__icontains=_search
            )

            items = (
                Item.objects.filter(query)
                .select_related("category")
                .order_by("category")
            )

        else:
            items = (
                Item.objects.all()
                .select_related("category")
                .order_by("category")
            )
        ctx = {"item_list": items, "search": _search}

        return render(
            request, template_name="menu/item_list.html", context=ctx
        )


class ItemDetailView(DetailView):
    model = Item


class OrderView(LoginRequiredMixin, ListView):
    model = Order

    def get(self, request, *args, **kwargs):
        if not hasattr(request.user, "table"):
            return render(request, "menu/no_table.html")

        order = (
            Table.objects.select_related("orders")
            .get(id=request.user.table.id)
            .get_order()
        )

        orderitem_list = order.get_items()

        ctx = {"order": order, "orderitem_list": orderitem_list}
        return render(
            request,
            "menu/order.html",
            ctx,
        )


class AddItemView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(
            request.META.get("HTTP_REFERER", reverse_lazy("menu:order"))
        )

    def post(self, request, item_id):
        order = Table.objects.get(id=request.user.table.id).get_order()
        order.add_item(item_id)

        return HttpResponseRedirect(
            request.META.get("HTTP_REFERER", reverse_lazy("menu:order"))
        )


class RemoveItemView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(
            request.META.get("HTTP_REFERER", reverse_lazy("menu:order"))
        )

    def post(self, request, item_id):
        order = Table.objects.get(id=request.user.table.id).get_order()
        order.remove_item(item_id)

        return HttpResponseRedirect(
            request.META.get("HTTP_REFERER", reverse_lazy("menu:order"))
        )


class OrderCheckoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        table = Table.objects.get(user_id=request.user.id)
        order = Order.objects.get(table_id=table.id, status="P")
        order.status = "A"
        order.modified_at = timezone.now()
        order.save()

        return HttpResponseRedirect("/")
