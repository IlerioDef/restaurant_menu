from django.db import models


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
        return f"{self.name}"

    class Meta:
        ordering = ['category',]

    @property
    def get_allergens(self):
        allergens = Allergen.objects.filter(item__id=self.id)
        print(allergens)
        if allergens:
            return allergens

        return None

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return "https://placehold.co/600x400.png"


class Chef(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Table(models.Model):
    """
    Table Model, by default the number of tables is 13. You may change the number of tables manually
    """

    def get_table_names():
        table_choices = []
        for x in range(1, 14):
            table_choices.append((f"{x}", f"Table #{x}"))
        return table_choices

    def get_table_status():
        status_options = {
            ("O", "Open"),
            ("C", "Closed"),
            ('R', "Reserved")

        }
        return status_options

    name = models.CharField(max_length=10,
                            choices=get_table_names())
    status = models.CharField(max_length=3,
                              choices=get_table_status())

    def __str__(self):
        return f"Table #{self.name}"


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
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # What exactly is under preparation
    quantity = models.IntegerField()  # How many items are under preparation
    status = models.CharField(
        max_length=2,
        choices=ORDER_STATUS_CHOICES,
        default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order # {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(db_default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total