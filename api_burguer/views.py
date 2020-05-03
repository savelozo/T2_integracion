from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from rest_framework.views import APIView
from .models import Ingredient, Burguer
from .serializers import IngredientSerializer, BurguerSerializer

@api_view(['GET', 'POST'])
def ingredient_list(request):

    if request.method == 'GET':
        queryset = Ingredient.objects.all()
        serializer = IngredientSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = IngredientSerializer(data=request.data)

        if serializer.is_valid():

            if request.data['nombre'] != '' and request.data['precio'] != '':
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response('Input inválido', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def ingredient_detail(request, id):

    try:
        int(id)

    except:
        print("NO SOY UN INT")
        return Response("ID inválido", status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        queryset = Ingredient.objects.filter(id=id)
        if len(queryset):
            serializer = IngredientSerializer(queryset[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Ingrediente inexistente', status=status.HTTP_404_NOT_FOUND)

    else:
        queryset = Ingredient.objects.filter(id=id)
        if len(queryset):

            ingredient_object = queryset[0]
            if len(ingredient_object.burguer_set.all()) == 0:
                ingredient_object.delete()
                return Response('Ingrediente eliminado', status=status.HTTP_200_OK)
            else:
                return Response('Ingrediente no se puede borrar, se encuentra presente en una hamburguesa', status=status.HTTP_409_CONFLICT)

        else:
            return Response('Ingrediente inexistente', status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def burguer_list(request):

    if request.method == 'GET':
        queryset = Burguer.objects.all()
        serializer = BurguerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
