from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from django.forms import ModelForm

from menu.models import Order, OrderItem


class OrderAddForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['name', 'quantity', 'price']
