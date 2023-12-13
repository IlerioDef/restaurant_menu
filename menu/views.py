from tkinter import Menu

from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from menu.models import Item


# Create your views here.

class ItemView(ListView):
    model = Item

