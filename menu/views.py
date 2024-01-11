from tkinter import Menu

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from menu.models import Item, Order, OrderItem


# Create your views here.

class ItemListView(View):
    template_name = 'menu/item_list.html'

    def get(self, request, *args, **kwargs):
        strval = request.GET.get("search", False)
        if strval:
            query = Q(name__icontains=strval)
            query.add(Q(description__icontains=strval), Q.OR)
            items = Item.objects.filter(query).select_related().distinct().order_by('category')
        else:
            items = Item.objects.all().order_by("category")
        ctx = {'item_list': items, "search": strval}

        return render(request, self.template_name, ctx)


class ItemDetailView(DetailView):
    model = Item


@login_required
def order(request):
    table = request.user.table
    order, _ = Order.objects.get_or_create(table=table)
    products = order.orderitem_set.all()

    print(table, order, products)
    ctx = {'products': products, "order": order, "table": table}
    return render(request, 'menu/order.html', ctx)


def order_add(request):
    pass

def order_delete(request):
    pass

def order_update(request):
    pass