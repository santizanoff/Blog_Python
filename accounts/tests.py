from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import Perfil, Profile
from posts.models import Post


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPassword123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name']
        )
        self.post = Post.objects.create(
            titulo='Post de prueba',
            contenido='Contenido para testing de permisos',
            autor='testuser',
            estado='publicado'
        )

    def test_perfil_creado_automaticamente_por_signals(self):
        """Verifica que el modelo Perfil se crea automáticamente al crear un User."""
        self.assertTrue(hasattr(self.user, 'perfil'))
        self.assertIsInstance(self.user.perfil, Perfil)
        self.assertIsInstance(self.user.perfil, Profile)

    def test_login_exitoso(self):
        """Verifica inicio de sesión exitoso."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'StrongPassword123!'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_exitoso(self):
        """Verifica cierre de sesión."""
        self.client.login(username='testuser', password='StrongPassword123!')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)

    def test_registro_usuario(self):
        """Verifica que un nuevo usuario puede registrarse y obtiene su perfil."""
        response = self.client.post(reverse('accounts:registro'), {
            'username': 'nuevousuario',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'email': 'nuevo@example.com',
            'password1': 'MiClaveSegura2026!',
            'password2': 'MiClaveSegura2026!'
        })
        self.assertEqual(response.status_code, 302)
        nuevo_user = User.objects.get(username='nuevousuario')
        self.assertTrue(hasattr(nuevo_user, 'perfil'))
        self.assertEqual(nuevo_user.email, 'nuevo@example.com')

    def test_vistas_protegidas_posts_redirigen_a_login(self):
        """Verifica que crear, editar y eliminar posts redirigen al login si no está autenticado."""
        # /posts/crear/
        resp_crear = self.client.get(reverse('posts:crear_post'))
        self.assertEqual(resp_crear.status_code, 302)
        self.assertIn('/accounts/login/', resp_crear.url)

        # /post/nuevo/ (alias de compatibilidad)
        resp_nuevo = self.client.get('/post/nuevo/')
        self.assertEqual(resp_nuevo.status_code, 302)
        self.assertIn('/accounts/login/', resp_nuevo.url)

        # /posts/<slug>/editar/
        resp_editar = self.client.get(reverse('posts:editar_post', kwargs={'slug': self.post.slug}))
        self.assertEqual(resp_editar.status_code, 302)
        self.assertIn('/accounts/login/', resp_editar.url)

        # /posts/<slug>/eliminar/
        resp_eliminar = self.client.get(reverse('posts:eliminar_post', kwargs={'slug': self.post.slug}))
        self.assertEqual(resp_eliminar.status_code, 302)
        self.assertIn('/accounts/login/', resp_eliminar.url)

    def test_vistas_publicas_posts(self):
        """Verifica que inicio, listado y detalle son accesibles anónimamente."""
        resp_inicio = self.client.get(reverse('posts:inicio'))
        self.assertEqual(resp_inicio.status_code, 200)

        resp_lista = self.client.get(reverse('posts:lista_posts'))
        self.assertEqual(resp_lista.status_code, 200)

        resp_detalle = self.client.get(reverse('posts:detalle_post', kwargs={'slug': self.post.slug}))
        self.assertEqual(resp_detalle.status_code, 200)

    def test_perfil_protegido_y_accesible_autenticado(self):
        """Verifica vista de perfil para usuario autenticado."""
        # Anónimo redirige a login
        resp_anon = self.client.get(reverse('accounts:perfil'))
        self.assertEqual(resp_anon.status_code, 302)

        # Autenticado accede con 200
        self.client.login(username='testuser', password='StrongPassword123!')
        resp_auth = self.client.get(reverse('accounts:perfil'))
        self.assertEqual(resp_auth.status_code, 200)
        self.assertContains(resp_auth, 'testuser')

    def test_editar_perfil_con_avatar(self):
        """Verifica actualización de datos de perfil y subida de avatar."""
        self.client.login(username='testuser', password='StrongPassword123!')
        
        # 1x1 GIF transparente
        tiny_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00'
            b'\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00'
            b'\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02'
            b'\x44\x01\x00\x3b'
        )
        avatar_file = SimpleUploadedFile("avatar.gif", tiny_gif, content_type="image/gif")

        response = self.client.post(reverse('accounts:editar_perfil'), {
            'first_name': 'Santiago',
            'last_name': 'Zanoff',
            'email': 'santiago@example.com',
            'biografia': 'Desarrollador Python y apasionado por Django.',
            'link_web': 'https://github.com/santizanoff',
            'avatar': avatar_file
        })
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Santiago')
        self.assertEqual(self.user.perfil.biografia, 'Desarrollador Python y apasionado por Django.')
        self.assertTrue(bool(self.user.perfil.avatar))
