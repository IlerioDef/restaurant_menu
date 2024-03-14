from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, F


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Categories'


class Allergen(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)  # this item contains XXXX

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
        ordering = ['category']

    @property
    def get_allergens(self):
        allergens = Allergen.objects.filter(item__id=self.id)
        if allergens:
            allergens_list = []
            for allergen in allergens:
                allergens_list.append(allergen.name)
            return allergens_list

        return None

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return "https://placehold.co/600x400.png"


class Chef(models.Model):
    @staticmethod
    def get_chef_status():
        status_options = {
            ("A", "Active"),
            ("N", "Not working"),
        }
        return status_options
    name = models.CharField(max_length=50)
    status = models.CharField(
        max_length=2,
        choices=get_chef_status(),
        default="N"
    )
    def __str__(self):
        return self.name


class Table(models.Model):
    """
    Table Model, by default the number of tables is 13. You may change the number of tables manually
    """

    @staticmethod
    def get_table_names():
        table_choices = []
        for x in range(1, 14):
            table_choices.append((f"{x}", f"Table #{x}"))
        return table_choices

    @staticmethod
    def get_table_status():
        status_options = {
            ("O", "Open"),
            ("C", "Closed"),
            ('R', "Reserved")

        }
        return status_options

    name = models.CharField(max_length=10,
                            choices=get_table_names())
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=3,
                              choices=get_table_status())

    def __str__(self):
        return f"Table {self.name}, user: {self.user}, status: {self.status}"


class Order(models.Model):
    PENDING = "P"
    ACCEPTED = "A"
    PROCESSING = "PR"
    DONE = "D"
    CANCELLED = "C"

    ORDER_STATUS_CHOICES = {
        PENDING: "Pending",
        ACCEPTED: "Accepted",
        PROCESSING: "Processing",
        DONE: "Done",
        CANCELLED: "Cancelled",
    }
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through="OrderItem", related_name="orders_items")
    status = models.CharField(
        max_length=2,
        choices=ORDER_STATUS_CHOICES,
        default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order # {self.id}"

    def get_order_total_amount(self):
        total = self.orderitem_set.aggregate(order_total_amount=Sum(F("item__price") * F("quantity")))
        return total['order_total_amount']

    def get_order_total_items(self):
        total = self.orderitem_set.aggregate(order_total_items=Sum('quantity'))
        return total['order_total_items']

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
