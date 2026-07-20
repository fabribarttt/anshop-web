from django.shortcuts import render, get_object_or_404
from .models import Categoria, Producto
from django.core.paginator import Paginator
from django.conf import settings


def home(request):

    categoria_slug = request.GET.get("categoria") or "estuches"

    productos = (
        Producto.objects.filter(categoria__slug=categoria_slug)
        .order_by("-id")
        .prefetch_related("imagenes")
    )

    paginator = Paginator(productos, settings.PAGE_SIZE)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    categorias_validas = Categoria.objects.filter(productos__isnull=False).distinct()

    context = {
        "page_obj": page_obj,
        "categoria_activa": categoria_slug,
        "categorias": categorias_validas,
    }

    # Si es solicitud HTMX, devolver solo el partial de tarjetas
    if request.headers.get("HX-Request") == "true":
        return render(request, "store/partials/product_cards.html", context)

    # Solicitud normal: renderizar página completa
    return render(request, "store/index.html", context)


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    context = {
        "producto": producto,
    }
    return render(request, "store/producto_detalle.html", context)
