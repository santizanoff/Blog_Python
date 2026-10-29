from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import Post


class PostCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='autor_test',
            password='Password123!',
            first_name='Autor',
            last_name='Test'
        )
        self.post_publicado = Post.objects.create(
            titulo='Publicación pública',
            contenido='Contenido del post publicado para pruebas.',
            autor='autor_test',
            estado='publicado'
        )
        self.post_borrador = Post.objects.create(
            titulo='Publicación borrador',
            contenido='Contenido en borrador.',
            autor='autor_test',
            estado='borrador'
        )

    def test_inicio_view(self):
        """La página de inicio carga correctamente para visitantes anónimos."""
        response = self.client.get(reverse('posts:inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Blog Consola')

    def test_acerca_view(self):
        """La página acerca de carga correctamente."""
        response = self.client.get(reverse('posts:acerca'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Santiago Zanoff')

    def test_lista_posts_anonimo(self):
        """Visitante anónimo puede ver la lista de posts publicados pero no borradores."""
        response = self.client.get(reverse('posts:lista_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Publicación pública')
        self.assertNotContains(response, 'Publicación borrador')

    def test_detalle_post_sin_imagen(self):
        """Detalle del post se renderiza correctamente incluso si no tiene imagen."""
        response = self.client.get(reverse('posts:detalle_post', kwargs={'slug': self.post_publicado.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post_publicado.titulo)
        self.assertContains(response, self.post_publicado.contenido)

    def test_detalle_post_con_imagen(self):
        """Detalle del post renderiza la imagen cuando existe."""
        img = SimpleUploadedFile('test.png', b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR', content_type='image/png')
        post_con_img = Post.objects.create(
            titulo='Post con imagen',
            contenido='Tiene una imagen adjunta.',
            autor='autor_test',
            estado='publicado',
            imagen=img
        )
        response = self.client.get(reverse('posts:detalle_post', kwargs={'slug': post_con_img.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post_con_img.imagen.url)

    def test_crear_post_requiere_login(self):
        """Usuario anónimo es redirigido al login al intentar crear un post."""
        url = reverse('posts:crear_post')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_editar_post_requiere_login(self):
        """Usuario anónimo es redirigido al login al intentar editar un post."""
        url = reverse('posts:editar_post', kwargs={'slug': self.post_publicado.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_eliminar_post_requiere_login(self):
        """Usuario anónimo es redirigido al login al intentar eliminar un post."""
        url = reverse('posts:eliminar_post', kwargs={'slug': self.post_publicado.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_crear_post_autenticado(self):
        """Usuario autenticado puede crear un post desde la web."""
        self.client.login(username='autor_test', password='Password123!')
        response = self.client.post(reverse('posts:crear_post'), {
            'titulo': 'Nuevo post desde test',
            'contenido': 'Contenido creado por usuario autenticado.',
            'autor': 'autor_test',
            'estado': 'publicado'
        })
        self.assertEqual(response.status_code, 302)
        nuevo_post = Post.objects.get(titulo='Nuevo post desde test')
        self.assertEqual(nuevo_post.estado, 'publicado')
        self.assertTrue(bool(nuevo_post.slug))

    def test_editar_post_autenticado(self):
        """Usuario autenticado puede editar un post existente."""
        self.client.login(username='autor_test', password='Password123!')
        response = self.client.post(reverse('posts:editar_post', kwargs={'slug': self.post_publicado.slug}), {
            'titulo': 'Título actualizado',
            'contenido': 'Contenido modificado.',
            'autor': 'autor_test',
            'estado': 'publicado'
        })
        self.assertEqual(response.status_code, 302)
        self.post_publicado.refresh_from_db()
        self.assertEqual(self.post_publicado.titulo, 'Título actualizado')
        self.assertEqual(self.post_publicado.contenido, 'Contenido modificado.')

    def test_eliminar_post_autenticado(self):
        """Usuario autenticado puede eliminar un post."""
        self.client.login(username='autor_test', password='Password123!')
        response = self.client.post(reverse('posts:eliminar_post', kwargs={'slug': self.post_publicado.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(id=self.post_publicado.id).exists())
