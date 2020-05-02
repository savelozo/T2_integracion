from django.db import models

class Ingredient(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)

class Burguer(models.Model):

    ingredients = models.ManyToManyField(Ingredient)
    id = models.IntegerField(primary_key=True)
    price = models.IntegerField()
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    image = models.CharField(max_length=256)
