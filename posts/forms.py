from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Formulario ModelForm para crear y editar publicaciones del blog."""

    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'autor', 'estado', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribí el título del post...',
                'id': 'id_titulo',
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribí el contenido aquí...',
                'rows': 10,
                'id': 'id_contenido',
            }),
            'autor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del autor',
                'id': 'id_autor',
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_estado',
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'id': 'id_imagen',
                'accept': 'image/*',
            }),
        }
        labels = {
            'titulo': 'Título',
            'contenido': 'Contenido',
            'autor': 'Autor',
            'estado': 'Estado',
            'imagen': 'Imagen destacada',
        }
        help_texts = {
            'imagen': 'Opcional. Formatos: JPG, PNG, WebP. La imagen se mostrará en el detalle del post.',
        }
