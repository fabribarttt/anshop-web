from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Categoria, Marca, ModeloDispositivo, Producto, Subcategoria


def home(request):
    # Obtenemos los parámetros garantizando que sean strings
    categoria_slug = request.GET.get("categoria") or ""
    subcategoria_slug = request.GET.get("subcategoria") or ""
    marca_slug = request.GET.get("marca") or ""
    modelo_slug = request.GET.get("modelo") or ""

    # Base Queryset
    productos = Producto.objects.all().prefetch_related(
        "imagenes", "modelos_dispositivo", "categoria", "subcategoria"
    )

    # Filtros condicionales independientes
    if categoria_slug and categoria_slug != "todas":
        productos = productos.filter(categoria__slug=categoria_slug)

    if subcategoria_slug:
        productos = productos.filter(subcategoria__slug=subcategoria_slug)

    if modelo_slug:
        productos = productos.filter(modelos_dispositivo__slug=modelo_slug)
    elif marca_slug:
        productos = productos.filter(modelos_dispositivo__marca__slug=marca_slug)

    # Evitar duplicados por ManyToMany
    productos = productos.distinct().order_by("-id")

    # Paginación con respaldo de seguridad
    page_size = getattr(settings, "PAGE_SIZE", 12)
    paginator = Paginator(productos, page_size)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Cargar selects
    categorias_validas = Categoria.objects.filter(productos__isnull=False).distinct()

    if categoria_slug and categoria_slug != "todas":
        subcategorias = Subcategoria.objects.filter(categoria__slug=categoria_slug)
    else:
        subcategorias = Subcategoria.objects.all()

    marcas = Marca.objects.all()

    # Modelos según marca elegida
    modelos_actuales = ModeloDispositivo.objects.none()
    if marca_slug:
        modelos_actuales = ModeloDispositivo.objects.filter(
            marca__slug=marca_slug
        ).order_by("nombre")

    context = {
        "page_obj": page_obj,
        "categoria_activa": categoria_slug,
        "subcategoria_activa": subcategoria_slug,
        "marca_activa": marca_slug,
        "modelo_activo": modelo_slug,
        "categorias": categorias_validas,
        "subcategorias": subcategorias,
        "marcas": marcas,
        "modelos": modelos_actuales,
    }

    if request.headers.get("HX-Request") == "true":
        return render(request, "store/partials/product_cards.html", context)

    return render(request, "store/index.html", context)


def cargar_modelos_filtro(request):
    marca_slug = request.GET.get("marca") or ""
    modelo_activo = request.GET.get("modelo") or ""

    if marca_slug:
        modelos = ModeloDispositivo.objects.filter(marca__slug=marca_slug).order_by(
            "nombre"
        )
    else:
        modelos = ModeloDispositivo.objects.none()

    return render(
        request,
        "store/partials/modelos_options.html",
        {
            "modelos": modelos,
            "modelo_activo": modelo_activo,
        },
    )


def producto_detalle(request, pk):
    producto = get_object_or_404(
        Producto.objects.prefetch_related("imagenes", "modelos_dispositivo__marca"),
        pk=pk,
    )
    context = {
        "producto": producto,
    }
    return render(request, "store/producto_detalle.html", context)
