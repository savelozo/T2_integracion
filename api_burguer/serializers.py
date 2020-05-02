from rest_framework import serializers
from .models import Ingredient, Burguer

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'description')
