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
    allergens = models.ManyToManyField(Allergen, blank=True)
    image = models.ImageField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - id: {self.id}"

    class Meta:
        ordering = ["category"]

    def get_allergens(self):
        return self.allergens.all()

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
    table = models.ForeignKey(
        "Table", on_delete=models.SET_NULL, null=True, blank=True
    )
    chef = models.ForeignKey(
        Chef, on_delete=models.SET_NULL, null=True, blank=True
    )
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

    def get_order(self, table_id):
        order, _ = Order.objects.get_or_create(
            table_id=table_id, status="PENDING"
        )

    def get_total_amount(self):
        total = self.orderitem_set.aggregate(
            total_amount=Sum(F("item__price") * F("quantity"))
        )
        return total["total_amount"]

    def get_total_items(self):
        total = self.orderitem_set.aggregate(total_items=Sum("quantity"))
        return total["total_items"]

    def get_order_allergens(self):
        return (
            self.orderitem_set.prefetch_related("item__allergies")
            .values_list("item__allergies__name", flat=True)
            .distinct()
        )

    def get_items(self):
        return self.orderitem_set.prefetch_related("item")

    def add_item(self, item_id):
        orderitem, created = self.orderitem_set.get_or_create(item_id=item_id)
        if created:
            return

        orderitem.quantity = F("quantity") + 1
        orderitem.save()

    def remove_item(self, item_id):
        orderitem = self.orderitem_set.get(item_id=item_id)
        orderitem.quantity = F("quantity") - 1
        orderitem.save()

        if self.orderitem_set.get(item_id=item_id).quantity == 0:
            orderitem.delete()


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
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(max_length=10, choices=TABLE_STATUS_CHOICES)

    def __str__(self):
        return f"Table {self.number}, user: {self.user}, status: {self.status}"

    def get_order(self):
        order, _ = Order.objects.get_or_create(table_id=self.id)

        return order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item, on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} Item {self.item} x {self.quantity} pcs."

    def get_total_amount(self):
        return self.item.price * self.quantity
