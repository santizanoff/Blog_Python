# 📝 Blog Consola — Blog Web con Django

Aplicación web de blog construida con Python y Django, desarrollada como proyecto integrador y final del curso de Introducción al Desarrollo Web con Python y Django. Evolucionó desde un prototipo en consola hasta una aplicación web completa con sistema de publicaciones, imágenes, autenticación de usuarios, perfiles y panel de administración.

---

## 🚀 Tecnologías utilizadas

| Tecnología | Versión | Descripción |
|---|---|---|
| **Python** | `3.14.7` | Lenguaje principal (compatible con `>= 3.10`) |
| **Django** | `6.1.1` | Framework web |
| **SQLite** | — | Base de datos en desarrollo |
| **Pillow** | `13.0.0` | Procesamiento de imágenes |
| **python-decouple** | `3.8` | Manejo de variables de entorno |
| **Bootstrap** | `5.3` | Framework CSS (CDN) |

---

## ✨ Funcionalidades principales

### Publicaciones (Posts)
- Listar todos los posts publicados con imagen destacada y resumen.
- Ver el detalle completo de un post.
- Crear, editar y eliminar posts desde la interfaz web (requiere sesión iniciada).
- Carga y visualización de imagen destacada; el template resiste si falta la imagen.
- Slugs automáticos en URLs para SEO amigable.

### Usuarios y Autenticación
- Registro de usuarios con validaciones de seguridad de Django.
- Login y logout con redirección inteligente.
- Perfil de usuario editable: biografía, avatar y sitio web personal.
- Cambio de contraseña seguro.
- Navegación dinámica: distingue usuario anónimo de autenticado.

### Seguridad y Rutas Protegidas
- Crear, editar y eliminar posts requieren sesión iniciada (`@login_required`).
- Editar perfil y cambiar contraseña requieren sesión iniciada.
- Los usuarios anónimos son redirigidos automáticamente al login.

### Panel de Administración
- Gestión completa de posts y usuarios desde `/admin/`.
- Vista inline de perfiles de usuario en el admin de Django.

---

## 📋 Requisitos Previos

- **Python** `3.14.x` (o `>= 3.10` / `3.12+` compatibles con Django 6.x)
  > El proyecto fue desarrollado y probado bajo **Python 3.14.7**.
- **pip** — incluido con la instalación de Python.
- **git** — para clonar el repositorio.

---

## ⚙️ Instalación y puesta en marcha

```bash
# 1. Clonar el repositorio
git clone https://github.com/santizanoff/Blog_Python.git
cd Blog_Python

# 2. Crear el entorno virtual
python -m venv venv

# 3. Activar el entorno virtual
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# En Windows (CMD):
venv\Scripts\activate.bat
# En macOS / Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
# Copiar el archivo de ejemplo y editar los valores
cp .env.example .env
# Editar .env con tu SECRET_KEY (ver instrucciones dentro del archivo)

# 6. Aplicar migraciones (crea la base de datos)
python manage.py migrate

# 7. Crear superusuario para el panel de administración
python manage.py createsuperuser

# 8. Iniciar el servidor de desarrollo
python manage.py runserver
```

Abrí el navegador en **http://127.0.0.1:8000/**

> **Nota**: Si no incluís un archivo `.env`, el proyecto igual arranca con valores predeterminados seguros para desarrollo (`DEBUG=True` y una `SECRET_KEY` de fallback). Para producción, siempre configurá tu propio `.env`.

---

## 🌐 Mapa de URLs

### Vistas Públicas (sin autenticación)
| URL | Descripción |
|---|---|
| `/` | Página de inicio |
| `/posts/` | Listado de publicaciones |
| `/posts/<slug>/` | Detalle de una publicación |
| `/acerca/` | Página "Acerca de" |
| `/accounts/login/` | Iniciar sesión |
| `/accounts/registro/` | Registrarse |

### Vistas Protegidas (`@login_required`)
| URL | Descripción |
|---|---|
| `/posts/crear/` | Crear nueva publicación |
| `/posts/<slug>/editar/` | Editar publicación |
| `/posts/<slug>/eliminar/` | Eliminar publicación |
| `/accounts/perfil/` | Ver mi perfil |
| `/accounts/perfil/editar/` | Editar perfil y avatar |
| `/accounts/password-change/` | Cambiar contraseña |
| `/accounts/logout/` | Cerrar sesión |
| `/admin/` | Panel de administración de Django |

---

## 📁 Estructura del proyecto

```
Blog_Python/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── blog_project/
│   ├── settings.py       # Configuración principal (usa python-decouple)
│   ├── urls.py           # Enrutador principal
│   ├── asgi.py
│   └── wsgi.py
│
├── posts/                # App de publicaciones
│   ├── models.py         # Modelo Post con ImageField y slug
│   ├── views.py          # Vistas CRUD con @login_required
│   ├── forms.py          # PostForm (ModelForm)
│   ├── urls.py           # Rutas CRUD
│   ├── admin.py
│   ├── migrations/
│   ├── templates/posts/
│   │   ├── base.html     # Template base con navbar condicional
│   │   ├── inicio.html
│   │   ├── acerca.html
│   │   ├── lista_posts.html
│   │   ├── detalle_post.html
│   │   ├── post_form.html
│   │   └── post_confirm_delete.html
│   └── static/posts/css/
│       └── estilos.css   # Estilos dark glassmorphism
│
└── accounts/             # App de autenticación y perfiles
    ├── models.py         # Modelo Perfil (OneToOne con User)
    ├── views.py          # Vistas de registro, login, logout y perfil
    ├── forms.py          # RegistroUsuarioForm, UserEditForm, PerfilForm
    ├── signals.py        # Crea Perfil automáticamente al crear User
    ├── urls.py
    ├── admin.py          # PerfilAdmin y PerfilInline
    ├── migrations/
    └── templates/accounts/
        ├── login.html
        ├── registro.html
        ├── perfil.html
        ├── editar_perfil.html
        └── password_change.html
```

---

## 🗄️ Base de datos y archivos de media

El repositorio **no incluye** `db.sqlite3` ni la carpeta `media/`. Para empezar desde cero:

```bash
# Crear la base de datos (ejecuta todas las migraciones)
python manage.py migrate

# Crear superusuario para acceder al panel de administración
python manage.py createsuperuser
```

La carpeta `media/` se crea automáticamente cuando subís imágenes desde la interfaz.

---

## 📈 Historial de evolución

| Hito / Módulo | Funcionalidades |
|---|---|
| Base del proyecto | Arquitectura base de Django, entorno virtual, app `posts` |
| Vistas y Templates | Rutas, vistas funcionales, templates modulares, CSS (MVT) |
| Modelo y Base de Datos | Modelo `Post`, ORM, migraciones SQLite, Panel de Admin |
| CRUD y Multimedia | CRUD completo de publicaciones, imágenes con Pillow |
| Autenticación y Perfiles | Registro, login, logout, modelo `Perfil` con avatar, rutas protegidas |
| **Entrega Final** | **Consolidación, documentación, variables de entorno, limpieza del repo** |

---

## 👤 Autor

**Santiago Zanoff**
- GitHub: [@santizanoff](https://github.com/santizanoff)
- Proyecto desarrollado como entrega final del curso de Python y Django — 2026
