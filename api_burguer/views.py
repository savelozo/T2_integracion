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
        return Response("ID inválido", status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':

        try:
            ingredient = Ingredient.objects.get(id=id)
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Ingredient.DoesNotExist:
            return Response('Ingrediente inexistente', status=status.HTTP_404_NOT_FOUND)


    else:
        try:
            ingredient = Ingredient.objects.get(id=id)

            if len(ingredient.burguer_set.all()) == 0:
                ingredient.delete()
                return Response('Ingrediente eliminado', status=status.HTTP_200_OK)
            else:
                return Response('Ingrediente no se puede borrar, se encuentra presente en una hamburguesa', status=status.HTTP_409_CONFLICT)

        except Ingredient.DoesNotExist:
            return Response('Ingrediente inexistente', status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def burguer_list(request):

    if request.method == 'GET':
        queryset = Burguer.objects.all()
        serializer = BurguerSerializer(queryset, many=True)

        for burguer_data in serializer.data:
            counter = 0
            for ingredient_id in burguer_data['ingredientes']:
                burguer_data['ingredientes'][counter] = {'path': 'https://hamburgueseria.com/ingrediente/{}'.format(ingredient_id)}
                counter += 1

        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = BurguerSerializer(data=request.data)

        if serializer.is_valid():

            if request.data['nombre'] != '' and request.data['precio'] != '' and request.data['descripcion'] != '' and request.data['imagen'] != '':
                object = serializer.save()
                data = {'id': object.id}
                data.update(serializer.data)
                return Response(data, status=status.HTTP_201_CREATED)

        return Response('Input inválido', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PATCH'])
def burguer_detail(request, id):

    try:
        int(id)

    except:
        return Response("ID inválido", status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':

        try:
            burguer = Burguer.objects.get(id=id)
            serializer = BurguerSerializer(burguer)
            counter = 0
            for ingredient_id in serializer.data['ingredientes']:
                serializer.data['ingredientes'][counter] = {'path': 'https://hamburgueseria.com/ingrediente/{}'.format(ingredient_id)}
                counter += 1
            data = {'id': burguer.id}
            data.update(serializer.data)
            return Response(data, status=status.HTTP_200_OK)

        except Burguer.DoesNotExist:
            return Response('Hamburguesa inexistente', status=status.HTTP_404_NOT_FOUND)


    elif request.method == 'DELETE':
        try:
            burguer = Burguer.objects.get(id=id)
            burguer.delete()
            return Response('Hamburguesa eliminada', status=status.HTTP_200_OK)

        except Burguer.DoesNotExist:
            return Response('Hamburguesa inexistente', status=status.HTTP_404_NOT_FOUND)

    else:
        data_update = request.data
        try:
            burguer_object = Burguer.objects.get(id=id)
            serializer = BurguerSerializer(burguer_object, data=request.data, partial=True)
            if serializer.is_valid() and id == data_update['id']:
                serializer.save()
                data = {'id': id}
                data.update(serializer.data)
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response('Parámetros inválidos', status=status.HTTP_400_BAD_REQUEST)

        except Burguer.DoesNotExist:
            return Response('Hamburguesa inexistente', status=status.HTTP_404_NOT_FOUND)
