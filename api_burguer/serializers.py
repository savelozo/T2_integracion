from rest_framework import serializers
from .models import Ingredient, Burguer

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id','nombre', 'descripcion')

class BurguerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Burguer
        fields = ('id','nombre', 'descripcion', 'precio', 'ingredientes','imagen')
