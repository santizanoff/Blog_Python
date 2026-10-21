from django.shortcuts import render
from .models import Post


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
    contexto = {
        'titulo_pagina': 'Publicaciones - Blog Consola',
        'posts': posts,
    }
    return render(request, 'posts/lista_posts.html', contexto)
