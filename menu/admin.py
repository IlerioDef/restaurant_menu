from django.contrib import admin

from menu.models import Allergen, Category, Chef, Item, Order, OrderItem, Table

# Register your models here.


admin.site.register(Allergen)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(Chef)
admin.site.register(OrderItem)
