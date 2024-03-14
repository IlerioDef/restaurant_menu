from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView

from menu.models import Item, OrderItem, Order, Table, Chef


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

        return render(request, template_name='menu/item_list.html', context=ctx)


class ItemDetailView(DetailView):
    model = Item


class OrderView(LoginRequiredMixin, ListView):
    model = Order

    def get(self, request, *args, **kwargs):
        table = Table.objects.get(user_id=request.user.id)
        chef = Chef.objects.get(status="A")
        order, _ = Order.objects.get_or_create(table_id=table.id, status="P", chef_id=chef.id)
        orderitem_list = order.orderitem_set.all()
        print(orderitem_list)
        return render(request, "menu/order.html",
                      {"table": table, "orderitem_list": orderitem_list, "order": order})


class OrderModifyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy("menu:order")))

    def post(self, request, *args, **kwargs):
        table = Table.objects.get(user_id=request.user.id)
        chef = Chef.objects.get(status="A")
        order, _ = Order.objects.get_or_create(table_id=table.id, status="P", chef_id=chef.id)

        if kwargs["action"] == "add":

            try:
                item_in_order = order.orderitem_set.all().get(item__id=kwargs['pk'])
                item_in_order.quantity += 1
                item_in_order.save()
            except OrderItem.DoesNotExist:
                item_in_order = order.orderitem_set.create(item_id=kwargs["pk"], quantity=1)
                item_in_order.save()

        elif kwargs["action"] == "remove":
            try:
                item_in_order = order.orderitem_set.all().get(item__id=kwargs['pk'])
                item_in_order.quantity -= 1
                item_in_order.save()
                if item_in_order.quantity == 0:
                    item_in_order.delete()
                    order.save()

            except ValueError as e:
                print("It does not exist", e)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy("menu:order")))


class OrderCheckoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        table = Table.objects.get(user_id=request.user.id)
        order = Order.objects.get(table_id=table.id, status="P")
        order.status = "A"
        order.modified_at = timezone.now()
        order.save()

        return HttpResponseRedirect("/")
