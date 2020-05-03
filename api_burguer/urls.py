
from django.urls import path, include
from . import views
#from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('ingrediente/', views.ingredient_list),
    path('ingrediente/<id>', views.ingredient_detail),
    path('hamburguesa/', views.burguer_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)


# from django.urls import path, include
# from . import views
#
#
# urlpatterns = [
#     path('ingrediente/', views.IngredientView),
#     path('hamburguesa/', views.BurguerView),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)
