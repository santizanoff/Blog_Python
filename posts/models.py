from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    """Modelo que representa una publicación del blog."""

    class Estado(models.TextChoices):
        BORRADOR = 'borrador', 'Borrador'
        PUBLICADO = 'publicado', 'Publicado'
        ARCHIVADO = 'archivado', 'Archivado'

    titulo = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name='Slug')
    contenido = models.TextField(verbose_name='Contenido')
    autor = models.CharField(max_length=100, verbose_name='Autor')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.BORRADOR,
        verbose_name='Estado',
    )
    imagen = models.ImageField(upload_to='posts/', null=True, blank=True, verbose_name='Imagen')

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
