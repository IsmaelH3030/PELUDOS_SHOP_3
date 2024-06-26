from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from PELUDOS_SHOP_APP.Carrito import Carrito
from django.utils import timezone
from django.db import transaction


# Create your views here.

def inicio(request):
    # Para que se muestren los platos que la empresa requeria de platos
#    user = request.user
    perfil = request.session.get('perfil')
#     if user.is_authenticated:
#         try:
#             user_profile = UserProfile.objects.get(user=user)
#             empresa = user_profile.empresa.first()  # Obtener la primera empresa asociada al perfil
#         except UserProfile.DoesNotExist:
#             user_profile = None
#             empresa = None

#         if empresa:
#             platos = empresa.platos_disponibles.filter(disponibilidad=True)
#         else:
#             platos = PlatoProveedor.objects.filter(disponibilidad=True)
#     else:
#         platos = PlatoProveedor.objects.filter(disponibilidad=True)

    platos = ProductoProveedor.objects.filter(stock__gt=0,disponibilidad=True)

    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'perfil': perfil,
        'platos': platos,
        'user_profile': user_profile,
    }

    return render(request, 'public/inicio.html', context)

def registro(request):
    if request.method == 'POST':
        us = request.POST.get('InputUsuario')
        correo = request.POST.get('InputEmail1')
        run = request.POST.get('run')
        contrasenia = request.POST.get('InputPassword1')
        role = 'cliente'

        if User.objects.filter(username=us).exists():
            messages.error(request, 'El usuario ya está en uso')
            return render(request, 'auth/registro.html')

        if User.objects.filter(email=correo).exists():
            messages.error(request, 'El correo ya está en uso')
            return render(request, 'auth/registro.html')

        if User.objects.filter(id=run).exists():
            messages.error(request, 'El rut ya está en uso')
            return render(request, 'auth/registro.html')

        # Verifica que 'us' no esté vacío o nulo antes de crear el usuario
        if not us:
            messages.error(request, 'El nombre de usuario es obligatorio')
            return render(request, 'auth/registro.html')

        user = User.objects.create_user(username=us, email=correo, password=contrasenia)

        UserProfile.objects.create(user=user, run=run, role=role)
        return redirect('inicio')
        # Resto de tu lógica aquí (redireccionar, etc.)

    return render(request, 'auth/registro.html')

def iniciosesion(request):
    error_message = None  # Variable para almacenar el mensaje de error
    if request.method == 'POST':
        usuario = request.POST['InputUsuario']  # Se obtiene el usuario
        contrasenia = request.POST['InputPassword1']  # Se obtiene la contraseña
        user = authenticate(request, username=usuario, password=contrasenia)  # Autenticar usuario
        if user is not None:
            profile = UserProfile.objects.get(user=user)  # Obtener el perfil del usuario
            request.session['perfil'] = profile.role  # Guardar el rol en la sesión
            auth_login(request, user)  # Iniciar sesión
            return redirect('inicio')  # Redirigir a la página de inicio
        else:
            error_message = 'Usuario o contraseña incorrectos, intente de nuevo.'  # Mensaje de error
    return render(request, 'auth/iniciosesion.html', {'error_message': error_message})  # Renderizar la página con mensaje de error

@login_required
@role_required('admin', 'cliente')
def logout_view(request):
    auth_logout(request)
    return redirect('inicio')

def detalle_plato(request, id):
    perfil = request.session.get('perfil')
    plato = get_object_or_404(ProductoProveedor, id=id)

    context = {
        'perfil': perfil,
        'plato': plato,
    }
    return render(request, 'public/detalle_plato.html', context)

# def carrito(request):
#     return render(request, 'public/carrito.html')


def carro(request):
    perfil = request.session.get('perfil')
    platos = ProductoProveedor.objects.filter(stock__gt=0,disponibilidad=True)

    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'perfil': perfil,
        'platos': platos,
        'user_profile': user_profile,

    }
    return render(request, "public/carrito.html",context)

def descrip_carro(request):
    return render(request, 'public/descrip_carrito.html')

def lista_productos(request):
    productos = ProductoProveedor.objects.all()  # Obtén todos los productos (ajusta la consulta según tu modelo)
    context = {
        'productos': productos,
    }
    return render(request, "carrito", context)

def agregar_producto(request, producto_id):
    v_carrito = Carrito(request)
    producto = ProductoProveedor.objects.get(id=producto_id)
    v_carrito.agregar(producto)
    return redirect("menu")

def eliminar_producto(request, producto_id):
    v_carrito = Carrito(request)
    producto = ProductoProveedor.objects.get(id=producto_id)
    v_carrito.eliminar(producto)
    return redirect("menu")

def restar_producto(request, producto_id):
    v_carrito = Carrito(request)
    producto = ProductoProveedor.objects.get(id=producto_id)
    v_carrito.restar(producto)
    return redirect("menu")

def limpiar_carrito(request):
    v_carrito = Carrito(request)
    v_carrito.limpiar()
    return redirect("menu")


@transaction.atomic
def pago(request):
    carrito = request.session.get('carrito', {})
    
    if not carrito:  # Verificar si el carrito está vacío
        return render(request, 'public/carrito.html', {'error': 'No existen productos en el carrito.'})
    
    if request.method == "POST":
        # Procesar la selección de despacho y método de pago
        despacho = request.POST.get('despacho', '')
        metodo_pago = request.POST.get('metodo_pago', '')
        
        # Validar dirección si se selecciona despacho a domicilio
        if despacho == 'domicilio':
            direccion = request.POST.get('direccion', '')
            if not direccion:
                messages.error(request, 'Debes ingresar una dirección para el despacho a domicilio.')
                return redirect('pago')
        else:
            direccion = None
        
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para realizar una compra.')
            return redirect('iniciosesion')  # Redirigir a la página de inicio de sesión
        
        # Obtener el UserProfile asociado al usuario actual
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            messages.error(request, 'Debes iniciar sesión antes de comprar.')
            return redirect('iniciosesion')  # O redirigir a la página de inicio si UserProfile no existe
        
        try:
            with transaction.atomic():
                # Validar si se paga con saldo
                if metodo_pago == 'saldo':
                    # Calcular el total de la compra
                    total_compra = sum(value['acumulado'] for key, value in carrito.items())
                    
                    # Verificar si el saldo es suficiente
                    if user_profile.saldo < total_compra:
                        messages.error(request, 'Saldo insuficiente para realizar la compra.')
                        return redirect('carrito')  # O redirigir a la página del carrito
                    
                    # Actualizar el saldo del usuario
                    user_profile.saldo -= total_compra
                    user_profile.save()
                
                # Guardar los detalles de la compra y actualizar el stock
                for key, value in carrito.items():
                    producto = ProductoProveedor.objects.get(id=value['producto_id'])
                    cantidad_comprada = value['cantidad']
                    precio_total = value['acumulado']
                    
                    # Validar si la cantidad deseada supera el stock disponible
                    if cantidad_comprada > producto.stock:
                        messages.error(request, f'El producto "{producto.nombre_producto}" no tiene suficiente stock disponible.')
                        return redirect('carrito')  # O redirigir a la página del carrito
                    
                    # Crear el detalle de la compra
                    DetalleCompra.objects.create(
                        producto=producto,
                        cantidad=cantidad_comprada,
                        precio_total=precio_total,
                        tipo_despacho=despacho,
                        direccion_entrega=direccion,
                        fecha_compra=timezone.now(),
                        usuario=user_profile,
                        metodo_pago=metodo_pago  # Guardar el método de pago
                    )
                    
                    # Actualizar el stock del producto
                    producto.stock -= cantidad_comprada
                    producto.save()
                
                # Limpiar el carrito después de la compra
                del request.session['carrito']
                request.session.modified = True
                
                return redirect('confirmacion')
        
        except ProductoProveedor.DoesNotExist:
            messages.error(request, 'Uno o más productos no existen en nuestro inventario.')
            return redirect('carrito')  # O redirigir a la página del carrito
        
        except Exception as e:
            messages.error(request, f'Ocurrió un error al procesar tu compra: {str(e)}')
            return redirect('carrito')  # O redirigir a la página del carrito

    perfil = request.session.get('perfil')
    platos = ProductoProveedor.objects.filter(stock__gt=0, disponibilidad=True)
    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'perfil': perfil,
        'platos': platos,
        'user_profile': user_profile,
    }
        
    return render(request, 'public/pago.html', context)


def confirmacion(request):
    perfil = request.session.get('perfil')


    platos = ProductoProveedor.objects.filter(stock__gt=0,disponibilidad=True)

    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'perfil': perfil,
        'platos': platos,
        'user_profile': user_profile,
    }

    return render(request, 'public/confirmacion.html',context )




def menu(request):
       # Para que se muestren los platos que la empresa requeria de platos
#    user = request.user
    perfil = request.session.get('perfil')
#     if user.is_authenticated:
#         try:
#             user_profile = UserProfile.objects.get(user=user)
#             empresa = user_profile.empresa.first()  # Obtener la primera empresa asociada al perfil
#         except UserProfile.DoesNotExist:
#             user_profile = None
#             empresa = None

#         if empresa:
#             platos = empresa.platos_disponibles.filter(disponibilidad=True)
#         else:
#             platos = PlatoProveedor.objects.filter(disponibilidad=True)
#     else:
#         platos = PlatoProveedor.objects.filter(disponibilidad=True)

    platos = ProductoProveedor.objects.filter(stock__gt=0,disponibilidad=True)

    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'perfil': perfil,
        'platos': platos,
        'user_profile': user_profile,
    }

    return render(request, 'menu.html', context)


def chile(request):
    return render(request, 'chile.html')

def italia(request):
    return render(request, 'italia.html')

def china(request):
    return render(request, 'china.html')

def nosotros(request):
               # Para que se muestren los platos que la empresa requeria de platos
#    user = request.user
    perfil = request.session.get('perfil')
#     if user.is_authenticated:
#         try:
#             user_profile = UserProfile.objects.get(user=user)
#             empresa = user_profile.empresa.first()  # Obtener la primera empresa asociada al perfil
#         except UserProfile.DoesNotExist:
#             user_profile = None
#             empresa = None

#         if empresa:
#             platos = empresa.platos_disponibles.filter(disponibilidad=True)
#         else:
#             platos = PlatoProveedor.objects.filter(disponibilidad=True)
#     else:
#         platos = PlatoProveedor.objects.filter(disponibilidad=True)

    platos = ProductoProveedor.objects.filter(stock__gt=0,disponibilidad=True)

    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'perfil': perfil,
        'platos': platos,
        'user_profile': user_profile,
    }
    return render(request, 'nosotros.html', context)

def peru(request):
    return render(request, 'peru.html')

def preguntasFrecuentes(request):
           # Para que se muestren los platos que la empresa requeria de platos
#    user = request.user
    perfil = request.session.get('perfil')
#     if user.is_authenticated:
#         try:
#             user_profile = UserProfile.objects.get(user=user)
#             empresa = user_profile.empresa.first()  # Obtener la primera empresa asociada al perfil
#         except UserProfile.DoesNotExist:
#             user_profile = None
#             empresa = None

#         if empresa:
#             platos = empresa.platos_disponibles.filter(disponibilidad=True)
#         else:
#             platos = PlatoProveedor.objects.filter(disponibilidad=True)
#     else:
#         platos = PlatoProveedor.objects.filter(disponibilidad=True)

    platos = ProductoProveedor.objects.filter(stock__gt=0,disponibilidad=True)

    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'perfil': perfil,
        'platos': platos,
        'user_profile': user_profile,
    }
    return render(request, 'preguntasFrecuentes.html', context)



