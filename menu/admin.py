from django.contrib import admin

# Register your models here.


from menu.models import Allergen, Category, Item

admin.site.register(Allergen)
admin.site.register(Category)
admin.site.register(Item)
