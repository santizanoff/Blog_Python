from django.db import models


class Post(models.Model):
    """Modelo que representa una publicación del blog."""

    class Estado(models.TextChoices):
        BORRADOR = 'borrador', 'Borrador'
        PUBLICADO = 'publicado', 'Publicado'
        ARCHIVADO = 'archivado', 'Archivado'

    titulo = models.CharField(max_length=200, verbose_name='Título')
    contenido = models.TextField(verbose_name='Contenido')
    autor = models.CharField(max_length=100, verbose_name='Autor')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.BORRADOR,
        verbose_name='Estado',
    )

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.titulo
