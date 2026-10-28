from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    """
    Modelo que extiende la información del usuario estándar de Django
    mediante una relación OneToOne.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name="Usuario"
    )
    biografia = models.TextField(
        blank=True,
        verbose_name="Biografía",
        help_text="Breve descripción o biografía del autor."
    )
    avatar = models.ImageField(
        upload_to='avatares/',
        blank=True,
        null=True,
        verbose_name="Avatar",
        help_text="Imagen de perfil (JPG, PNG, WebP)."
    )
    link_web = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Sitio Web",
        help_text="Enlace a tu sitio web, portfolio o red social."
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"Perfil de {self.user.username}"


# Alias 'Profile' para compatibilidad con convenciones en inglés
Profile = Perfil
