from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('redireccion/', views.redireccion_por_rol, name='redireccion'),
    path('cliente/', views.vista_cliente, name='vista_cliente'),
    path('registro/', views.registro_cliente, name='registro_cliente'),
    path('vendedor/', views.vista_vendedor, name='vista_vendedor'),
    path('bodeguero/', views.vista_bodeguero, name='vista_bodeguero'),
    path('bodeguero/preparar/<int:orden_id>/', views.preparar_orden, name='preparar_orden'),
    path('contador/', views.vista_contador, name='vista_contador'),
    path('cliente/catalogo/', views.ver_catalogo, name='ver_catalogo'),
    path('cliente/confirmar_pedido/', views.procesar_pedido, name='procesar_pedido'),
    path('vendedor/pedidos/', views.gestion_pedidos_vendedor, name='gestion_pedidos_vendedor'),
    path('vendedor/pedidos/aprobar/<int:pedido_id>/', views.aprobar_pedido, name='aprobar_pedido'),
    path('vendedor/pedidos/rechazar/<int:pedido_id>/', views.rechazar_pedido, name='rechazar_pedido'),
    path('vendedor/pedidos/detalle/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),

    

]
