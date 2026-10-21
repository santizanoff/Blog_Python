# Blog Django

Proyecto de blog desarrollado con Django, evolucionando desde un prototipo en consola hasta una aplicación web con base de datos real.

## Descripción

Repositorio que implementa la arquitectura MVT de Django con modelo `Post`, panel de administración, ORM y renderizado dinámico de publicaciones desde SQLite.

## Stack

- Python 3.x
- Django 4.x
- SQLite (base de datos local)

## Instalación y Ejecución

1. Clonar el repositorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\Activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Aplicar migraciones:
```bash
python manage.py migrate
```

5. Crear superusuario (para acceder al admin):
```bash
python manage.py createsuperuser
```

6. Ejecutar servidor de desarrollo:
```bash
python manage.py runserver
```

## Panel de Administración

Una vez creado el superusuario, podés acceder al panel administrativo en:

```
http://127.0.0.1:8000/admin/
```

Desde allí podés crear, editar y eliminar posts. Los posts con estado **"Publicado"** aparecerán dinámicamente en la página de publicaciones del blog.

## Estructura del Proyecto

```
blog_django/
├── manage.py
├── requirements.txt
├── db.sqlite3          # generado localmente tras migrate
├── blog_project/
│   ├── settings.py
│   └── urls.py
└── posts/
    ├── models.py       # Modelo Post con ORM
    ├── admin.py        # PostAdmin registrado
    ├── views.py        # Vista lista_posts con ORM
    ├── urls.py
    ├── migrations/
    ├── templates/posts/
    │   ├── base.html
    │   ├── inicio.html
    │   ├── lista_posts.html
    │   └── acerca.html
    └── static/posts/css/
        └── estilos.css
```

## Checkpoints completados

| Módulo | Descripción |
|--------|-------------|
| 7 | Entorno virtual, proyecto Django e app `posts` |
| 8 | Rutas, vistas, templates y archivos estáticos (MVT) |
| **9** | **Modelo Post, migraciones, admin y ORM** |