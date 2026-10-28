from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil


class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario personalizado para el registro de nuevos usuarios en el blog,
    solicitando nombre, apellido, correo electrónico y credenciales.
    """
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@dominio.com'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if 'class' not in self.fields[field_name].widget.attrs:
                self.fields[field_name].widget.attrs['class'] = 'form-control'


class UserEditForm(forms.ModelForm):
    """
    Formulario para editar los datos básicos del usuario (nombre, apellido, email).
    """
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PerfilForm(forms.ModelForm):
    """
    Formulario para editar la biografía, el avatar y el enlace web del Perfil.
    """
    class Meta:
        model = Perfil
        fields = ('biografia', 'avatar', 'link_web')
        labels = {
            'biografia': 'Biografía',
            'avatar': 'Imagen de Avatar',
            'link_web': 'Sitio Web o Portfolio',
        }
        widgets = {
            'biografia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Contanos brevemente sobre vos, tus intereses o tu experiencia...'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
            'link_web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://tusitio.com'
            }),
        }
