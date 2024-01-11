from django.contrib import admin

# Register your models here.


from menu.models import Allergen, Category, Item, Table, Order, Chef, OrderItem

admin.site.register(Allergen)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(Chef)
admin.site.register(OrderItem)

