from .models import Categoria


def categorias_all(request):
    categorias = Categoria.objects.all()
    return {"categorias": categorias}
