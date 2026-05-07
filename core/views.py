from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria


def home(request):
    productos = Producto.objects.all().prefetch_related("imagenes")
    categorias = Categoria.objects.all()
    context = {
        "productos": productos,
        "categorias": categorias,
    }
    return render(request, "store/index.html", context)


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria
    ).exclude(pk=pk)[:3]
    context = {
        "producto": producto,
        "productos_relacionados": productos_relacionados,
    }
    return render(request, "store/producto_detalle.html", context)
