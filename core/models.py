from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    slug = models.SlugField(blank=True, unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Subcategoria(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="subcategorias"
    )
    nombre = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.categoria.nombre} > {self.nombre}"


class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(blank=True, unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class ModeloDispositivo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="modelos")
    nombre = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    precio = models.IntegerField()
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, related_name="productos"
    )

    modelos_dispositivo = models.ManyToManyField(
        ModeloDispositivo, blank=True, related_name="productos"
    )

    subcategoria = models.ForeignKey(
        Subcategoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
    )

    def __str__(self):
        return self.nombre


class ProductoImagen(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="imagenes"
    )
    imagen = models.ImageField(upload_to="productos/")
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"
