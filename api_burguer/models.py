from django.db import models

class Ingredient(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=256)
    descripcion = models.CharField(max_length=256)

    def __str__(self):
        return self.nombre

class Burguer(models.Model):

    id = models.IntegerField(primary_key=True)
    ingredientes = models.ManyToManyField(Ingredient)
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=256)
    nombre = models.CharField(max_length=256)
    imagen = models.CharField(max_length=256)

    def __str__(self):
        return self.nombre
