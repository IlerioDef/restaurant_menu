from tkinter import Menu

from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from menu.models import Item


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
            items = Item.objects.all().order_by()
        ctx = {'item_list': items, "search": strval}

        return render(request, self.template_name, ctx)


class ItemDetailView(DetailView):
    model = Item
