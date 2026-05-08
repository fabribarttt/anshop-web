from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria
from django.core.paginator import Paginator
from django.conf import settings


def home(request):
    productos = Producto.objects.all().order_by("id").prefetch_related("imagenes")
    categorias = Categoria.objects.all()

    paginator = Paginator(productos, settings.PAGE_SIZE)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "categorias": categorias,
    }

    # Si es solicitud HTMX, devolver solo el partial de tarjetas
    if request.headers.get("HX-Request"):
        return render(request, "store/partials/product_cards.html", context)

    # Solicitud normal: renderizar página completa
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
