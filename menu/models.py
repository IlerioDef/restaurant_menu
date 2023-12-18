import django.db.models
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
        ordering = ['category']

    def get_allergens(self):
        allergens = Allergen.objects.filter(item__id = self.id)
        print(allergens)
        if allergens:
            return allergens

        return None
