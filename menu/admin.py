from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from menu.models import Allergen, Category, Chef, Item, Order, OrderItem, Table

# Register your models here.


admin.site.register(Allergen)
admin.site.register(Category)
admin.site.register(Chef)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Table)


class TableInline(admin.StackedInline):
    model = Table
    can_delete = False
    verbose_name_plural = "tables"


class UserAdmin(BaseUserAdmin):
    inlines = [TableInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
