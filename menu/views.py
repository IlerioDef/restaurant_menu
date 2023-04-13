from django.shortcuts import render
from .models import FoodsForSale


# Create your views here.
def frontpage(request):
    foods = FoodsForSale.objects.all()[0:5]
    return render(request, "menu/frontpage.html", {
        "foods": foods,
    })
