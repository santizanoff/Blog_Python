from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post
from .forms import PostForm


def inicio(request):
    """Vista para la página de inicio del blog."""
    contexto = {
        'titulo_pagina': 'Inicio - Blog Consola',
        'mensaje_bienvenida': '¡Bienvenido a Blog Consola!',
        'descripcion_proyecto': 'Un proyecto creado para aprender y dominar el desarrollo web con Python y Django, evolucionando desde un prototipo en consola hacia una plataforma moderna.',
    }
    return render(request, 'posts/inicio.html', contexto)


def acerca(request):
    """Vista para la página Acerca de."""
    contexto = {
        'titulo_pagina': 'Acerca de - Blog Consola',
        'autor': 'Santiago Zanoff',
        'bio_autor': 'Apasionado por la programación en Python, la ciencia de datos y el desarrollo de aplicaciones web.',
        'proposito_sitio': 'El propósito de este sitio es documentar el aprendizaje, compartir conocimientos sobre tecnología y aplicar las mejores prácticas del ecosistema Django.',
    }
    return render(request, 'posts/acerca.html', contexto)


def lista_posts(request):
    """Vista para mostrar publicaciones publicadas del blog desde la base de datos."""
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_creacion')
    # Garantizar que ningún post antiguo tenga slug vacío para evitar NoReverseMatch
    for p in posts:
        if not p.slug:
            p.save()
    contexto = {
        'titulo_pagina': 'Publicaciones - Blog Consola',
        'posts': posts,
    }
    return render(request, 'posts/lista_posts.html', contexto)


def detalle_post(request, slug):
    """Vista para mostrar el detalle de un post individual."""
    post = get_object_or_404(Post, slug=slug)
    contexto = {
        'titulo_pagina': f'{post.titulo} - Blog Consola',
        'post': post,
    }
    return render(request, 'posts/detalle_post.html', contexto)


from django.contrib.auth.decorators import login_required


@login_required
def crear_post(request):
    """Vista protegida para crear un nuevo post desde el formulario web."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, f'✅ Post "{post.titulo}" creado exitosamente.')
            return redirect('posts:detalle_post', slug=post.slug)
    else:
        autor_inicial = request.user.get_full_name() or request.user.username
        form = PostForm(initial={'autor': autor_inicial})

    contexto = {
        'titulo_pagina': 'Crear Post - Blog Consola',
        'form': form,
        'accion': 'Crear',
        'titulo_formulario': 'Nueva publicación',
    }
    return render(request, 'posts/post_form.html', contexto)


@login_required
def editar_post(request, slug):
    """Vista protegida para editar un post existente."""
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, f'✏️ Post "{post.titulo}" actualizado correctamente.')
            return redirect('posts:detalle_post', slug=post.slug)
    else:
        form = PostForm(instance=post)

    contexto = {
        'titulo_pagina': f'Editar: {post.titulo} - Blog Consola',
        'form': form,
        'post': post,
        'accion': 'Guardar cambios',
        'titulo_formulario': f'Editando: {post.titulo}',
    }
    return render(request, 'posts/post_form.html', contexto)


@login_required
def eliminar_post(request, slug):
    """Vista protegida para confirmar y eliminar un post."""
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        titulo = post.titulo
        post.delete()
        messages.success(request, f'🗑️ Post "{titulo}" eliminado correctamente.')
        return redirect('posts:lista_posts')

    contexto = {
        'titulo_pagina': f'Eliminar: {post.titulo} - Blog Consola',
        'post': post,
    }
    return render(request, 'posts/post_confirm_delete.html', contexto)
