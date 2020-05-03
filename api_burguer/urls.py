
from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('ingrediente/', views.ingredient_list),
    path('ingrediente', views.ingredient_list),
    path('ingrediente/<id>', views.ingredient_detail),
    path('hamburguesa/', views.burguer_list),
    path('hamburguesa', views.burguer_list),
    path('hamburguesa/<id>', views.burguer_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
