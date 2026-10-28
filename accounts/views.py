from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Perfil
from .forms import RegistroUsuarioForm, UserEditForm, PerfilForm


class CustomLoginView(LoginView):
    """
    Vista de inicio de sesión que renderiza el formulario estilizado
    y redirige a los usuarios ya autenticados.
    """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"¡Hola de nuevo, {form.get_user().username}! Has iniciado sesión.")
        return super().form_valid(form)


def cerrar_sesion(request):
    """
    Cierra la sesión del usuario tanto por GET como por POST y redirige con un mensaje de despedida.
    """
    if request.user.is_authenticated:
        nombre = request.user.username
        logout(request)
        messages.info(request, f"Hasta luego, {nombre}. Has cerrado sesión correctamente.")
    return redirect('posts:lista_posts')


def registro(request):
    """
    Vista para el registro de nuevos usuarios.
    Crea el usuario, inicializa su perfil OneToOne y lo autentica directamente.
    """
    if request.user.is_authenticated:
        return redirect('posts:lista_posts')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Asegura la creación del perfil OneToOne
            Perfil.objects.get_or_create(user=user)
            login(request, user)
            messages.success(
                request,
                f"¡Bienvenido/a {user.username}! Tu cuenta ha sido creada exitosamente."
            )
            return redirect('accounts:perfil')
    else:
        form = RegistroUsuarioForm()

    contexto = {
        'titulo_pagina': 'Registro de Usuario - Blog Consola',
        'form': form,
    }
    return render(request, 'accounts/registro.html', contexto)


@login_required
def perfil_usuario(request):
    """
    Vista protegida que muestra el perfil y datos del usuario autenticado.
    """
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    contexto = {
        'titulo_pagina': f'Perfil de {request.user.username} - Blog Consola',
        'perfil': perfil,
    }
    return render(request, 'accounts/perfil.html', contexto)


@login_required
def editar_perfil(request):
    """
    Vista protegida para editar datos de usuario (nombre, apellido, email)
    y del perfil (biografía, avatar, enlace web).
    """
    perfil, _ = Perfil.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, "✅ Tu perfil ha sido actualizado correctamente.")
            return redirect('accounts:perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil)

    contexto = {
        'titulo_pagina': 'Editar Perfil - Blog Consola',
        'user_form': user_form,
        'perfil_form': perfil_form,
        'perfil': perfil,
    }
    return render(request, 'accounts/editar_perfil.html', contexto)


class CustomPasswordChangeView(PasswordChangeView):
    """
    Vista protegida para cambiar la contraseña del usuario.
    """
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:perfil')

    def form_valid(self, form):
        messages.success(self.request, "🔑 Tu contraseña ha sido modificada con éxito.")
        return super().form_valid(form)
