from django.db import models
from usuarios.models import Usuario
from productos.models import Producto

class Pedido(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'CLIENTE'})
    fecha = models.DateTimeField(auto_now_add=True)
    direccion_envio = models.TextField()
    retiro_en_tienda = models.BooleanField(default=True)
    aprobado = models.BooleanField(default=False)
    tipo_entrega = models.CharField(
        max_length=20,
        choices=[
            ('RETIRO', 'Retiro en tienda'),
            ('DOMICILIO', 'Despacho a domicilio')
        ],
        default='RETIRO'
    )

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class OrdenPreparacion(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    preparado = models.BooleanField(default=False)
    fecha_preparacion = models.DateTimeField(null=True, blank=True)
    bodeguero = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'rol': 'BODEGUERO'})

    def __str__(self):
        return f"Orden de Preparación para Pedido #{self.pedido.id}"
