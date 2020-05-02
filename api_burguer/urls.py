
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('ingrediente', views.IngredientView)
#router.register('hamburguesa', views.IngredientView)

urlpatterns = [
    path('', include(router.urls)),
]
