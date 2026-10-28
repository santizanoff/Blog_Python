# Blog Consola - Django Blog

Proyecto de blog desarrollado con Python y Django, evolucionando desde un prototipo en consola hasta una aplicación web completa con CRUD, imágenes y administración de contenido.

---

## Cómo ejecutar el proyecto

```bash
# 1. Clonar el repositorio
git clone https://github.com/santizanoff/Pre_Entrega_7_Django.git
cd Pre_Entrega_7_Django
# (O si se clonó especificando el nombre de carpeta 'Blog_consola': cd Blog_consola)

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

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear superusuario (opcional, para el panel admin)
python manage.py createsuperuser

# 6. Ejecutar el servidor de desarrollo
python manage.py runserver
```

### 🌐 Rutas de arranque en el navegador

Con el servidor corriendo, podés acceder a las rutas clave de la aplicación:

- **🏠 Inicio / Portada**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) - Página principal con acceso directo a todas las secciones.
- **📰 Publicaciones (CRUD)**: [http://127.0.0.1:8000/posts/](http://127.0.0.1:8000/posts/) - Listado de posts publicados con enlaces a ver, editar y eliminar.
- **✍️ Crear Publicación**: [http://127.0.0.1:8000/posts/crear/](http://127.0.0.1:8000/posts/crear/) - Formulario con subida de imágenes destacadas.
- **ℹ️ Acerca de**: [http://127.0.0.1:8000/acerca/](http://127.0.0.1:8000/acerca/) - Información sobre el autor y el propósito del blog.
- **⚙️ Panel Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) - Panel administrativo nativo de Django.

---

## Operaciones CRUD disponibles

El sistema CRUD permite gestionar publicaciones directamente desde el sitio web, sin necesidad del panel de administración.

| Operación | URL | Descripción |
|-----------|-----|-------------|
| **Listar** | `/posts/` | Lista todos los posts publicados |
| **Detalle** | `/posts/<slug>/` | Ver el detalle completo de un post |
| **Crear** | `/posts/crear/` | Formulario para nueva publicación |
| **Editar** | `/posts/<slug>/editar/` | Formulario para editar un post existente |
| **Eliminar** | `/posts/<slug>/eliminar/` | Confirmar y eliminar un post |

---

## Configuración del manejo de imágenes

Se utilizan los ajustes `MEDIA_URL` y `MEDIA_ROOT` en `blog_project/settings.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Las imágenes subidas por usuarios se almacenan en `media/posts/`.

En `blog_project/urls.py` se sirven los archivos media durante el desarrollo con:

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Nueva dependencia instalada: Pillow

`Pillow` es la librería de procesamiento de imágenes requerida por Django para usar `ImageField`.

```bash
pip install Pillow
```

Incluida en `requirements.txt`.

---

## Cómo probar la carga de imágenes

1. Ir a [http://127.0.0.1:8000/posts/crear/](http://127.0.0.1:8000/posts/crear/)
2. Completar el formulario: título, autor, contenido, estado
3. En el campo **"Imagen destacada"**, seleccionar una imagen local (JPG, PNG, WebP)
4. Hacer clic en **"Crear"**
5. La imagen se guarda en `media/posts/` y se muestra en la vista de detalle
6. Para editar la imagen, ir a `/posts/<slug>/editar/` y seleccionar una nueva imagen

> **Nota**: El atributo `enctype="multipart/form-data"` en el formulario es crítico para que la imagen llegue al servidor.

---

## Estructura del proyecto

```
Blog_consola/
│
├── manage.py
├── README.md
├── requirements.txt
│
├── blog_project/
│   ├── settings.py       # MEDIA_URL, MEDIA_ROOT
│   └── urls.py           # static() para media en dev
│
├── media/
│   └── posts/            # Imágenes subidas por usuarios
│
└── posts/
    ├── admin.py
    ├── forms.py          # PostForm (ModelForm)
    ├── models.py         # Post con ImageField y slug
    ├── urls.py           # Rutas CRUD
    ├── views.py          # Vistas CRUD
    │
    ├── templates/
    │   └── posts/
    │       ├── base.html
    │       ├── inicio.html
    │       ├── acerca.html
    │       ├── lista_posts.html
    │       ├── detalle_post.html
    │       ├── post_form.html
    │       └── post_confirm_delete.html
    │
    └── static/
        └── posts/
            └── css/
                └── estilos.css
```

---

## Historial de módulos

| Módulo | Tema |
|--------|------|
| 7 | Proyecto Django base |
| 8 | Rutas → Vistas → Templates → Estáticos |
| 9 | Modelo Post, ORM, Panel Admin |
| **10** | **CRUD completo + imágenes (Preentrega actual)** |