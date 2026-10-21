from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Configuración del panel admin para el modelo Post."""

    list_display = ('titulo', 'autor', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('titulo', 'autor', 'contenido')
    ordering = ('-fecha_creacion',)
    list_per_page = 20
