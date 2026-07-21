from django.urls import path
from .views import home, producto_detalle
from . import views

urlpatterns = [
    path("", home, name="home"),
    path(
        "ajax/cargar-modelos/",
        views.cargar_modelos_filtro,
        name="cargar_modelos_filtro",
    ),
    path("producto/<int:pk>/", producto_detalle, name="producto_detalle"),
]
