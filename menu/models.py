from django.db import models


# Create your models here.
class Allergen(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FoodsForSale(models.Model):
    dish = models.CharField(max_length=255)
    price = models.IntegerField()
    allergens = models.ManyToManyField(Allergen)
    course = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.dish
