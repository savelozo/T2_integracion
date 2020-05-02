from django.shortcuts import render
from rest_framework import viewsets
from .models import Ingredient, Burguer
from .serializers import IngredientSerializer

# Create your views here.
class IngredientView(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
