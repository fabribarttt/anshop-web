from django.urls import path
from .views import home, producto_detalle

urlpatterns = [
    path("", home, name="home"),
    path("producto/<int:pk>/", producto_detalle, name="producto_detalle"),
]
