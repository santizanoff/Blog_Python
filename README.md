# Blog Consola - Django Blog

Proyecto de blog desarrollado con Python y Django, evolucionando desde un prototipo en consola hasta una aplicación web completa con CRUD, manejo de imágenes multimedia, sistema de autenticación de usuarios, perfiles personalizados con avatar y protección de vistas.

---

## Cómo ejecutar el proyecto

```bash
# 1. Clonar el repositorio
git clone https://github.com/santizanoff/Blog_Python.git
cd Blog_Python
# (O si tu carpeta local se llama 'Blog_consola': cd Blog_consola)

# 2. Crear y activar entorno virtual
python -m venv venv

# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# En Windows (CMD):
venv\Scripts\activate.bat
# En macOS / Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear y aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 5. Crear superusuario (opcional, para el panel admin)
python manage.py createsuperuser

# 6. Ejecutar el servidor de desarrollo
python manage.py runserver
```

---

## 🌐 Rutas del sitio y mapa de URLs

Con el servidor corriendo (`http://127.0.0.1:8000/`), podés acceder a las siguientes secciones:

### Vistas Públicas (Acceso libre)
- **🏠 Inicio / Portada**: [`/`](http://127.0.0.1:8000/) - Presentación del blog y accesos principales.
- **📰 Publicaciones**: [`/posts/`](http://127.0.0.1:8000/posts/) - Listado de posts publicados con enlace a ver detalle.
- **📖 Detalle de Post**: [`/posts/<slug>/`](http://127.0.0.1:8000/posts/primer-post/) - Lectura completa del artículo e imagen destacada.
- **ℹ️ Acerca de**: [`/acerca/`](http://127.0.0.1:8000/acerca/) - Información sobre el autor y el propósito del sitio.
- **🔐 Iniciar Sesión**: [`/accounts/login/`](http://127.0.0.1:8000/accounts/login/) (o acceso directo [`/login/`](http://127.0.0.1:8000/login/)).
- **✍️ Registrarse**: [`/accounts/registro/`](http://127.0.0.1:8000/accounts/registro/).

### Vistas Protegidas (Requieren autenticación - `@login_required`)
Si un usuario anónimo intenta acceder directamente por URL a cualquiera de estas vistas, Django lo redirige de forma automática a la pantalla de login:
- **✍️ Crear Post**: [`/posts/crear/`](http://127.0.0.1:8000/posts/crear/) (también disponible mediante el alias [`/post/nuevo/`](http://127.0.0.1:8000/post/nuevo/)).
- **✏️ Editar Post**: `/posts/<slug>/editar/` - Modificación de título, autor, estado, imagen y contenido.
- **🗑️ Eliminar Post**: `/posts/<slug>/eliminar/` - Pantalla de confirmación y eliminación física.
- **👤 Mi Perfil**: [`/accounts/perfil/`](http://127.0.0.1:8000/accounts/perfil/) - Visualización de datos de autor, avatar, biografía y sitio web.
- **⚙️ Editar Perfil & Avatar**: [`/accounts/perfil/editar/`](http://127.0.0.1:8000/accounts/perfil/editar/) - Edición de datos personales, biografía y subida de avatar.
- **🔑 Cambiar Contraseña**: [`/accounts/password-change/`](http://127.0.0.1:8000/accounts/password-change/) - Cambio de contraseña seguro.
- **🚪 Cerrar Sesión**: [`/accounts/logout/`](http://127.0.0.1:8000/accounts/logout/) (o acceso directo [`/logout/`](http://127.0.0.1:8000/logout/)).

---

## 👥 Sistema de Autenticación, Usuarios y Perfil (Preentrega 11)

### 1. Registro de Usuarios
- Implementado a través del formulario `RegistroUsuarioForm` basado en `UserCreationForm`.
- Solicita `username`, `first_name`, `last_name`, `email` y contraseña con confirmación y validaciones de seguridad de Django.
- Al enviar el formulario, el usuario se crea y automáticamente se inicializa su `Perfil` mediante una señal (`post_save` signal). Luego se inicia su sesión inmediatamente para una experiencia de usuario fluida.

### 2. Login y Logout
- **Login**: Utiliza la vista `CustomLoginView` extendida de `LoginView` de `django.contrib.auth.views`, con soporte para redirección automática tras iniciar sesión (`LOGIN_REDIRECT_URL = 'posts:lista_posts'`) y preservación del parámetro `?next=` para volver a la página solicitada previamente.
- **Logout**: Utiliza `cerrar_sesion` que permite cerrar sesión tanto por petición POST como GET, enviando un mensaje informativo y redirigiendo a la lista de publicaciones (`LOGOUT_REDIRECT_URL`).

### 3. Modelo `Perfil` (OneToOne con `User`)
Para extender la información de cada autor sin alterar el modelo nativo `User`, se diseñó el modelo `Perfil` en la app `accounts`:

```python
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    biografia = models.TextField(blank=True, verbose_name="Biografía")
    avatar = models.ImageField(upload_to='avatares/', blank=True, null=True, verbose_name="Avatar")
    link_web = models.URLField(max_length=255, blank=True, null=True, verbose_name="Sitio Web")
```

- **Creación automática**: Mediante señales en `accounts/signals.py`, cada vez que se crea un usuario en el sistema (por registro web, admin o `createsuperuser`), se crea automáticamente su respectivo `Perfil`.
- **Compatibilidad**: Se define el alias `Profile = Perfil` para garantizar compatibilidad total con cualquier entorno o evaluación.
- **Administración**: Registrado en `accounts/admin.py` tanto de forma independiente como inline (`PerfilInline`) dentro del panel de `UserAdmin`.

### 4. Configuración de Avatares y Archivos Multimedia
- Los avatares subidos se guardan en la carpeta `media/avatares/`.
- El proyecto tiene configurado en `blog_project/settings.py`:
  ```python
  MEDIA_URL = '/media/'
  MEDIA_ROOT = BASE_DIR / 'media'
  ```
- En `blog_project/urls.py` se sirven estáticamente los archivos en entorno de desarrollo.
- En los formularios de perfil se utiliza `enctype="multipart/form-data"` y la vista procesa `request.FILES` junto a una previsualización interactiva en JavaScript.

### 5. Navegación Dinámica Condicional
La barra de navegación (`posts/templates/posts/base.html`) se adapta en tiempo real:
- **Usuario Invitado (Anónimo)**: Ve enlaces a Inicio, Publicaciones, Acerca de, **Iniciar Sesión** y **Registrarse**.
- **Usuario Autenticado**: Ve enlace a **✍️ Nuevo Post**, un badge con su **avatar e indicación "Hola, {username}"**, acceso directo a **Mi Perfil** y botón para **Cerrar Sesión**.

---

## 🛠️ Ejecución de Migraciones

Para aplicar los cambios del modelo `Perfil` y la base de datos:

```bash
# Detectar modelos nuevos y cambios en apps
python manage.py makemigrations

# Aplicar las migraciones a la base de datos SQLite
python manage.py migrate
```

---

## 📁 Estructura del proyecto

```
Blog_Python / Blog_consola/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── blog_project/
│   ├── __init__.py
│   ├── settings.py           # MEDIA_URL, MEDIA_ROOT, LOGIN_URL, LOGIN_REDIRECT_URL
│   ├── urls.py               # Enrutador principal, static(MEDIA) y rutas de accounts
│   ├── asgi.py
│   └── wsgi.py
│
├── media/
│   ├── posts/                # Imágenes de publicaciones
│   └── avatares/             # Avatares de perfiles de usuario
│
├── posts/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py              # PostForm (ModelForm)
│   ├── models.py             # Post con ImageField y slug
│   ├── urls.py               # Rutas CRUD y alias /post/nuevo/
│   ├── views.py              # Vistas protegidas con @login_required
│   ├── tests.py
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── 0002_post_imagen_post_slug.py
│   │
│   ├── templates/posts/
│   │   ├── base.html         # Template base con navbar condicional y mensajes
│   │   ├── inicio.html
│   │   ├── acerca.html
│   │   ├── lista_posts.html
│   │   ├── detalle_post.html
│   │   ├── post_form.html
│   │   └── post_confirm_delete.html
│   │
│   └── static/posts/css/
│       └── estilos.css       # Estilos completos en CSS moderno (dark glassmorphism)
│
└── accounts/
    ├── admin.py              # PerfilAdmin y PerfilInline
    ├── apps.py               # AccountsConfig con carga de signals
    ├── forms.py              # RegistroUsuarioForm, UserEditForm, PerfilForm
    ├── models.py             # Modelo Perfil con OneToOneField a User
    ├── signals.py            # Signal post_save para creación automática de Perfil
    ├── urls.py               # Rutas de login, logout, registro, perfil y password
    ├── views.py              # Vistas de autenticación y gestión de perfil
    ├── tests.py              # Tests unitarios automatizados
    ├── migrations/
    │   └── 0001_initial.py   # Migración inicial del modelo Perfil
    │
    └── templates/accounts/
        ├── login.html        # Formulario de inicio de sesión
        ├── registro.html     # Formulario de registro con validaciones
        ├── perfil.html       # Vista detallada de perfil de autor y avatar
        ├── editar_perfil.html# Formulario con carga de avatar y request.FILES
        └── password_change.html # Cambio seguro de clave
```

---

## 📈 Historial de evolución del proyecto

| Hito / Módulo | Funcionalidades implementadas |
|---------------|-------------------------------|
| Base del proyecto | Arquitectura base de Django, configuración del entorno virtual y app `posts` |
| Vistas y Templates | Rutas, vistas basadas en funciones, plantillas modulares y estilos CSS (MVT) |
| Modelo y Base de Datos | Modelo `Post`, ORM, migraciones SQLite y Panel de Administración |
| CRUD y Multimedia | CRUD completo de publicaciones y carga de imágenes destacadas con Pillow |
| **Preentrega 11 (Actual)** | **Sistema de autenticación, registro de usuarios, modelo `Perfil` (OneToOne) con biografía y avatar, vistas protegidas con `@login_required` y navegación condicional** |