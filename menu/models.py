from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Sum

from restaurant_menu import settings


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Categories"


class Allergen(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    calories = models.IntegerField()
    allergies = models.ManyToManyField(Allergen, blank=True)
    image = models.ImageField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - id: {self.id}"

    class Meta:
        ordering = ["category"]

    @property
    def get_allergens(self):
        allergens = Allergen.objects.filter(item__id=self.id)
        if allergens:
            allergens_list = []
            for allergen in allergens:
                allergens_list.append(allergen.number)
            return allergens_list

        return None

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url

        return "https://placehold.co/600x400.png"


class Chef(models.Model):
    ON_DUTY = "ON DUTY"
    OFF_DUTY = "OFF DUTY"
    CHEF_STATUS_CHOICES = {
        ON_DUTY: "On Duty",
        OFF_DUTY: "Off Duty",
    }

    name = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10, choices=CHEF_STATUS_CHOICES, default=ON_DUTY
    )

    def __str__(self):
        return self.name


class Table(models.Model):
    """
    Table Model, by default the number of tables is 13.
    You may change the number of tables manually
    """

    OPEN = "OPEN"
    CLOSED = "CLOSED"
    TABLE_STATUS_CHOICES = {
        OPEN: "Open",
        CLOSED: "Closed",
    }

    def get_table_numbers():
        table_choices = []
        for x in range(1, settings.NUMBER_OF_TABLES + 1):
            table_choices.append((f"{x}", f"Table #{x}"))
        return table_choices

    number = models.CharField(max_length=10, choices=get_table_numbers())
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.CharField(max_length=10, choices=TABLE_STATUS_CHOICES)

    def __str__(self):
        return f"Table {self.number}, user: {self.user}, status: {self.status}"


class Order(models.Model):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

    ORDER_STATUS_CHOICES = {
        PENDING: "Pending",
        ACCEPTED: "Accepted",
        PROCESSING: "Processing",
        DONE: "Done",
        CANCELLED: "Cancelled",
    }
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    items = models.ManyToManyField(
        Item, through="OrderItem", related_name="orders_items"
    )
    status = models.CharField(
        max_length=15, choices=ORDER_STATUS_CHOICES, default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Order # {self.id}"

    def get_order_total_amount(self):
        total = self.orderitem_set.aggregate(
            order_total_amount=Sum(F("item__price") * F("quantity"))
        )
        return total["order_total_amount"]

    def get_order_total_items(self):
        total = self.orderitem_set.aggregate(order_total_items=Sum("quantity"))
        return total["order_total_items"]

    def get_order_allergens(self):
        order_items = self.orderitem_set.all()
        total = []
        for item in order_items:
            total = total + item.item.get_allergens
        total = list(set(total))
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} Item {self.item} x {self.quantity} pcs."

    def get_item_total(self):
        return self.item.price * self.quantity
