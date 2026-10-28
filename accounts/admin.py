from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Perfil


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'
    fk_name = 'user'


class CustomUserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'link_web', 'tiene_avatar')
    search_fields = ('user__username', 'user__email', 'biografia')
    list_filter = ('user__is_staff', 'user__is_active')

    def tiene_avatar(self, obj):
        return bool(obj.avatar)
    tiene_avatar.boolean = True
    tiene_avatar.short_description = "Avatar"


# Re-registrar UserAdmin para incluir el perfil inline
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
