from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from productos.models import Producto
from usuarios.models import Usuario
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from pedidos.models import OrdenPreparacion, Pedido, DetallePedido
import json
from django.utils import timezone

@login_required
def redireccion_por_rol(request):
    rol = request.user.rol
    if rol == 'ADMIN':
        return redirect('/admin/')
    elif rol == 'CLIENTE':
        return redirect('/usuarios/cliente/')
    elif rol == 'VENDEDOR':
        return redirect('/usuarios/vendedor/')
    elif rol == 'BODEGUERO':
        return redirect('/usuarios/bodeguero/')
    elif rol == 'CONTADOR':
        return redirect('/usuarios/contador/')
    else:
        return redirect('/usuarios/login/')

def es_cliente(usuario):
    return usuario.rol == 'CLIENTE'

@login_required
@user_passes_test(es_cliente)
def vista_cliente(request):
    return render(request, 'usuarios/panel_cliente.html', {
        'titulo': 'Cliente',
        'rol': 'Cliente',
    })

@login_required
@user_passes_test(es_cliente)
def ver_catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'usuarios/catalogo.html', {
        'productos': productos,
        'rol': 'Cliente',
        'titulo': 'Catálogo de Productos'
    })


def registro_cliente(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = make_password(request.POST['password'])

        Usuario.objects.create(
            username=username,
            email=email,
            password=password,
            rol='CLIENTE'
        )
        return redirect('login')

    return render(request, 'usuarios/registro.html')

def es_vendedor(usuario):
    return usuario.rol == 'VENDEDOR'

@login_required
@user_passes_test(es_vendedor)
def vista_vendedor(request):
    return render(request, 'usuarios/panel_vendedor.html', {
        'titulo': 'Vendedor',
        'rol': 'Vendedor',
    })

@login_required
@user_passes_test(es_vendedor)
def gestion_pedidos_vendedor(request):
    pedidos_pendientes = Pedido.objects.filter(aprobado=False)
    return render(request, 'usuarios/pedidos_vendedor.html', {
        'titulo': 'Pedidos pendientes',
        'rol': 'Vendedor',
        'pedidos': pedidos_pendientes
    })

@login_required
@user_passes_test(es_vendedor)
def aprobar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.aprobado = True
    pedido.save()

    # Crear la orden de preparación si no existe
    if not hasattr(pedido, 'ordenpreparacion'):
        OrdenPreparacion.objects.create(pedido=pedido)

    return redirect('gestion_pedidos_vendedor')

@login_required
@user_passes_test(es_vendedor)
def rechazar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.delete()
    return redirect('gestion_pedidos_vendedor')

@login_required
@user_passes_test(es_vendedor)
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = pedido.detalles.select_related('producto').all()
    return render(request, 'usuarios/detalle_pedido.html', {
        'pedido': pedido,
        'detalles': detalles
    })

def es_bodeguero(usuario):
    return usuario.rol == 'BODEGUERO'

@login_required
@user_passes_test(es_bodeguero)
def vista_bodeguero(request):
    ordenes = OrdenPreparacion.objects.filter(preparado=False)
    return render(request, 'usuarios/panel_bodeguero.html', {
        'titulo': 'Bodeguero',
        'rol': 'Bodeguero',
        'ordenes': ordenes,
    })

@login_required
@user_passes_test(es_bodeguero)
def preparar_orden(request, orden_id):
    orden = get_object_or_404(OrdenPreparacion, id=orden_id)
    orden.preparado = True
    orden.fecha_preparacion = timezone.now()
    orden.bodeguero = request.user
    orden.save()
    return redirect('vista_bodeguero')

def es_contador(usuario):
    return usuario.rol == 'CONTADOR'

@login_required
@user_passes_test(es_contador)
def vista_contador(request):
    return render(request, 'usuarios/panel_contador.html', {
        'titulo': 'Contador',
        'rol': 'Contador',
    })

def inicio(request):
    return render(request, 'usuarios/inicio.html')

@login_required
@user_passes_test(es_cliente)
def procesar_pedido(request):
    if request.method == 'POST':
        tipo_entrega = request.POST.get('tipo_entrega')
        productos_json = request.POST.get('productos')
        productos = json.loads(productos_json)

        pedido = Pedido.objects.create(
            cliente=request.user,
            fecha=timezone.now(),
            direccion_envio="Por definir",
            retiro_en_tienda=(tipo_entrega == 'RETIRO'),
            tipo_entrega=tipo_entrega,
            aprobado=False
        )

        for item in productos:
            producto_id = item['id']
            nombre = item['nombre']
            precio = item['precio']

            DetallePedido.objects.create(
                pedido=pedido,
                producto_id=producto_id,
                cantidad=1,  # En este flujo aún no hay selección de cantidad
                valor_unitario=precio
            )

        return redirect('vista_cliente')
    
