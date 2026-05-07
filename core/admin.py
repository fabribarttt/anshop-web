from django.contrib import admin
from .models import Producto, ProductoImagen, Categoria


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 3
    max_num = 20
    fields = ("imagen", "principal")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [ProductoImagenInline]
    list_display = ("nombre", "precio", "categoria")


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)


@admin.register(ProductoImagen)
class ProductoImagenAdmin(admin.ModelAdmin):
    list_display = ("producto", "principal")
