from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('CLIENTE', 'Cliente'),
        ('VENDEDOR', 'Vendedor'),
        ('BODEGUERO', 'Bodeguero'),
        ('CONTADOR', 'Contador'),
    ]
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='CLIENTE')

    def __str__(self):
        return f'{self.username} ({self.get_rol_display()})'

