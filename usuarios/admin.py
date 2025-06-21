from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol', 'rut')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('rol', 'rut')}),
    )


