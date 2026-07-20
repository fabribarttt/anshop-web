from django.contrib import admin
from django.db import models
from .models import (
    Producto,
    ProductoImagen,
    Categoria,
    Subcategoria,
    Marca,
    ModeloDispositivo,
)
from django.contrib.admin.widgets import FilteredSelectMultiple


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 3
    max_num = 20
    fields = ("imagen", "principal")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [ProductoImagenInline]
    list_display = ("nombre", "precio", "categoria")

    formfield_overrides = {
        models.ManyToManyField: {
            "widget": FilteredSelectMultiple(verbose_name="Modelos", is_stacked=False)
        },
    }


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)


@admin.register(ProductoImagen)
class ProductoImagenAdmin(admin.ModelAdmin):
    list_display = ("producto", "principal")


@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria")


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)


@admin.register(ModeloDispositivo)
class ModeloDispositivoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "marca")
