from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'), 
    path('registro/', views.registro, name='registro'),
    path('inicio/', views.iniciosesion, name = "iniciosesion"),
    path('logout/', views.logout_view, name='logout'), #
    path('menu/', views.menu, name='menu'),
    path('chile/', views.chile, name='chile'),
    path('italia/', views.italia, name='italia'),
    path('china/', views.china, name='china'),
    path('peru/', views.peru, name='peru'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('preguntasFrecuentes/', views.preguntasFrecuentes, name='preguntasFrecuentes'),
    path('plato/<int:id>/', views.detalle_plato, name='detalle_plato'), # Se define la URL para la vista de detalle de producto.
    path('carrito/', views.carro, name='carrito'),
    path('descrip-carrito/', views.descrip_carro, name='descrip-carrito'),
    path('agregar/<int:producto_id>/', views.agregar_producto, name='add'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='del'),
    path('restar/<int:producto_id>/', views.restar_producto, name='sub'),
    path('limpiar/', views.limpiar_carrito, name='cls'),
    path('pago/', views.pago, name='pago'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),
]
