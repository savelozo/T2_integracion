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

            if request.data['nombre'] != '' and request.data['descripcion'] != '':
                serializer.save()
                ingredient = Ingredient.objects.last()
                data = {'id': ingredient.id}
                data.update(serializer.data)
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

            for key in data_update:
                if key not in ['nombre', 'precio', 'descripcion', 'imagen']:
                    return Response('Parámetros inválidos', status=status.HTTP_400_BAD_REQUEST)

            serializer = BurguerSerializer(burguer_object, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()


                if serializer.data['ingredientes']:
                    counter = 0
                    for ingredient_id in serializer.data['ingredientes']:
                        serializer.data['ingredientes'][counter] = {'path': 'https://hamburgueseria.com/ingrediente/{}'.format(ingredient_id)}
                        counter += 1
                data = {'id': burguer_object.id}
                data.update(serializer.data)

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response('Parámetros inválidos', status=status.HTTP_400_BAD_REQUEST)

        except Burguer.DoesNotExist:
            return Response('Hamburguesa inexistente', status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE', 'PUT'])
def burguer_and_ingredients(request, id, ing_id):

    try:
        int(id)

    except:
        return Response("ID de hamburguesa inválido", status=status.HTTP_400_BAD_REQUEST)

    try:
        int(ing_id)

    except:
        return Response("ID de ingrediente inválido", status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':

        try:
            burguer = Burguer.objects.get(id=id)
            serializer = BurguerSerializer(burguer)

            if int(ing_id) in serializer.data['ingredientes']:
                try:
                    ingrediente = Ingredient.objects.get(id=ing_id)
                    burguer.ingredientes.remove(ingrediente)
                    new_serializer = BurguerSerializer(burguer)

                    counter = 0
                    for ingredient_id in new_serializer.data['ingredientes']:
                        new_serializer.data['ingredientes'][counter] = {'path': 'https://hamburgueseria.com/ingrediente/{}'.format(ingredient_id)}
                        counter += 1
                    data = {'id': burguer.id}
                    data.update(new_serializer.data)

                    return Response(data, status=status.HTTP_200_OK)

                except Ingredient.DoesNotExist:
                    return Response("Ingrediente inexistente en la hamburguesa", status=status.HTTP_404_NOT_FOUND)
            else:
                return Response('Ingrediente inexistente en la hamburguesa', status=status.HTTP_404_NOT_FOUND)

        except Burguer.DoesNotExist:
            return Response("ID de hamburguesa inválido", status=status.HTTP_400_BAD_REQUEST)

    else:

        try:
            burguer = Burguer.objects.get(id=id)
            serializer = BurguerSerializer(burguer)
            serializer.data['ingredientes']

            try:
                ingrediente = Ingredient.objects.get(id=ing_id)
                burguer.ingredientes.add(ingrediente)
                new_serializer = BurguerSerializer(burguer)

                counter = 0
                for ingredient_id in new_serializer.data['ingredientes']:
                    new_serializer.data['ingredientes'][counter] = {'path': 'https://hamburgueseria.com/ingrediente/{}'.format(ingredient_id)}
                    counter += 1
                data = {'id': burguer.id}
                data.update(new_serializer.data)

                return Response(data, status=status.HTTP_200_OK)

            except Ingredient.DoesNotExist:
                return Response("Ingrediente inexistente", status=status.HTTP_404_NOT_FOUND)

        except Burguer.DoesNotExist:
            return Response("ID de hamburguesa inválido", status=status.HTTP_400_BAD_REQUEST)
