from django.contrib import admin
from .models import Pedido, DetallePedido

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [DetallePedidoInline]
    list_display = ('cliente', 'fecha', 'aprobado', 'retiro_en_tienda')

admin.site.register(DetallePedido)
