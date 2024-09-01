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

def suscripcion(request):
    perfil = request.session.get('perfil')
    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'perfil': perfil,
        'user_profile': user_profile,
    }
    return render(request, 'suscripcion.html',context )



def inicio(request):
    
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

    return render(request, 'public/inicio.html', context)

def registro(request):
    error_message = None
    if request.method == 'POST':
        us = request.POST.get('InputUsuario')
        correo = request.POST.get('InputEmail1')
        run = request.POST.get('run')
        contrasenia = request.POST.get('InputPassword1')
        role = 'cliente'

        # Verificar si el usuario ya existe
        if User.objects.filter(username=us).exists():
            messages.error(request, 'El usuario ya está en uso')
            return render(request, 'auth/registro.html')

        # Verificar si el correo ya está en uso
        if User.objects.filter(email=correo).exists():
            messages.error(request, 'El correo ya está en uso')
            return render(request, 'auth/registro.html')

        # Verificar si el RUT ya está en uso
        if UserProfile.objects.filter(run=run).exists():
            messages.error(request, 'El rut ya está en uso')
            return render(request, 'auth/registro.html')

        # Verificar que el nombre de usuario no esté vacío
        if not us:
            messages.error(request, 'El nombre de usuario es obligatorio')
            return render(request, 'auth/registro.html')

        # Validación de longitud del RUT (mínimo 9 caracteres)
        if len(run) < 9 or len(run) > 10:
            messages.error(request, 'El RUT debe tener entre 9 a 10 caracteres')
            return render(request, 'auth/registro.html')

        # Crear el usuario si todo está correcto
        user = User.objects.create_user(username=us, email=correo, password=contrasenia)

        # Crear el perfil del usuario asociado con su RUT y rol
        UserProfile.objects.create(user=user, run=run, role=role)

        # Redirigir a la página de inicio después de completar el registro
        return redirect('inicio')

    # Renderizar el formulario de registro si la solicitud no es POST
    return render(request, 'auth/registro.html' ,{'error_message': error_message})

def iniciosesion(request):
    if request.method == 'POST':
        usuario = request.POST['InputUsuario']
        contrasenia = request.POST['InputPassword1']
        user = authenticate(request, username=usuario, password=contrasenia)
        if user is not None:
            profile = UserProfile.objects.get(user=user)
            request.session['perfil'] = profile.role
            auth_login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos, intente de nuevo.')  # Usar sistema de mensajes
    return render(request, 'auth/iniciosesion.html')

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

    if not request.user.is_authenticated:
        messages.warning(request, 'Debes iniciar sesión para realizar una compra.')
        return redirect('iniciosesion')  # Redirigir a la página de inicio de sesión

    # Obtener perfil y productos para mostrar en el formulario de pago
    perfil = request.session.get('perfil')
    platos = ProductoProveedor.objects.filter(stock__gt=0, disponibilidad=True)
    user_profile = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None

    context = {
        'perfil': perfil,
        'platos': platos,
        'user_profile': user_profile,
    }

    if request.method == "POST":
        # Procesar la selección de método de pago
        metodo_pago = request.POST.get('metodo_pago', '')

        # Validar que se haya seleccionado método de pago
        if not metodo_pago:
            messages.error(request, 'Debes ingresar el método de pago.')
            return render(request, 'public/pago.html', context)

        # Validar campos de tarjeta de débito si se selecciona este método de pago
        if metodo_pago == 'debito':
            nombre_titular_debito = request.POST.get('nombre_titular_debito', '')
            numero_tarjeta_debito = request.POST.get('numero_tarjeta_debito', '')
            cvv_debito = request.POST.get('cvv_debito', '')
            fecha_vencimiento_debito = request.POST.get('fecha_vencimiento_debito', '')

            if not (nombre_titular_debito and numero_tarjeta_debito and cvv_debito and fecha_vencimiento_debito):
                messages.error(request, 'Por favor completa todos los campos de la tarjeta de débito.')
                return render(request, 'public/pago.html', context)

            # Agregar los datos de tarjeta de débito al contexto para mantenerlos en el formulario
            context['nombre_titular_debito'] = nombre_titular_debito
            context['numero_tarjeta_debito'] = numero_tarjeta_debito
            context['cvv_debito'] = cvv_debito
            context['fecha_vencimiento_debito'] = fecha_vencimiento_debito

        # Validar campos de tarjeta de crédito si se selecciona este método de pago
        elif metodo_pago == 'credito':
            nombre_titular_credito = request.POST.get('nombre_titular_credito', '')
            numero_tarjeta_credito = request.POST.get('numero_tarjeta_credito', '')
            cvv_credito = request.POST.get('cvv_credito', '')
            fecha_vencimiento_credito = request.POST.get('fecha_vencimiento_credito', '')

            if not (nombre_titular_credito and numero_tarjeta_credito and cvv_credito and fecha_vencimiento_credito):
                messages.error(request, 'Por favor completa todos los campos de la tarjeta de crédito.')
                return render(request, 'public/pago.html', context)

            # Agregar los datos de tarjeta de crédito al contexto para mantenerlos en el formulario
            context['nombre_titular_credito'] = nombre_titular_credito
            context['numero_tarjeta_credito'] = numero_tarjeta_credito
            context['cvv_credito'] = cvv_credito
            context['fecha_vencimiento_credito'] = fecha_vencimiento_credito

        # Guardar los detalles de la compra y actualizar el stock
        try:
            with transaction.atomic():
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
                        tipo_despacho='retiro_tienda',  # Se establece como retiro en tienda
                        direccion_entrega=None,  # No se usa despacho a domicilio
                        fecha_compra=timezone.now(),
                        usuario=request.user.userprofile if request.user.is_authenticated else None,
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
    perfil = request.session.get('perfil')
    user_profile = None

    # Obtener productos filtrados por categoría
    productos_gatos = ProductoProveedor.objects.filter(categoria='comida_gatos', stock__gt=0, disponibilidad=True)
    productos_perros = ProductoProveedor.objects.filter(categoria='comida_perros', stock__gt=0, disponibilidad=True)
    accesorios = ProductoProveedor.objects.filter(categoria='accesorios', stock__gt=0, disponibilidad=True)

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'perfil': perfil,
        'productos_gatos': productos_gatos,
        'productos_perros': productos_perros,
        'accesorios': accesorios,
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
    return render(request, 'nosotros.html', context)

def peru(request):
    return render(request, 'peru.html')

def preguntasFrecuentes(request):
         
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
    return render(request, 'preguntasFrecuentes.html', context)


def crud(request):
    perfil = request.session.get('perfil')
    platos = ProductoProveedor.objects.filter(stock__gt=0, disponibilidad=True)
    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    productos = ProductoProveedor.objects.all()
    context = {
        'productos': productos,
        'perfil': perfil,
        'platos': platos,
        'user_profile': user_profile,
    }
    return render(request, 'productos/productos_list.html', context)


def productosAdd(request):
    perfil = request.session.get('perfil')
    platos = ProductoProveedor.objects.filter(stock__gt=0, disponibilidad=True)
    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    if request.method != "POST":
        proveedores = Proveedor.objects.all()
        categorias = ProductoProveedor.CATEGORIAS  # Obtén las opciones de categoría desde el modelo
        context = {
            'proveedores': proveedores,
            'categorias': categorias,  # Pasa las categorías al contexto
            'perfil': perfil,
            'platos': platos,
            'user_profile': user_profile,
        }
        return render(request, 'productos/productos_add.html', context)
    else:
        # Procesar el formulario POST para agregar el producto
        proveedor_id = request.POST.get("proveedor")
        nombre_producto = request.POST.get("nombre_producto")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        stock = request.POST.get("stock")
        disponibilidad = request.POST.get("disponibilidad")
        imagen = request.FILES.get("imagen")  # Usar request.FILES para obtener archivos
        categoria = request.POST.get("categoria")

        objProveedor = Proveedor.objects.get(id=proveedor_id)  # Corrige el campo id_proveedor a id

        # Crear el nuevo objeto ProductoProveedor con los datos recibidos
        ProductoProveedor.objects.create(
            proveedor=objProveedor,
            nombre_producto=nombre_producto,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            disponibilidad=disponibilidad,
            imagen=imagen,
            categoria=categoria
        )

        # Preparar el contexto con un mensaje de éxito
        context = {
            'mensaje': 'Datos grabados',
            'perfil': perfil,
            'platos': platos,
            'user_profile': user_profile,
        }
        return render(request, 'productos/productos_add.html', context)


def productos_del(request, pk):
    perfil = request.session.get('perfil')
    platos = ProductoProveedor.objects.filter(stock__gt=0, disponibilidad=True)
    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    context = {}
    try:
        producto = ProductoProveedor.objects.get(id=pk)
        producto.delete()
        mensaje = "Ok. Datos eliminados"
    except ProductoProveedor.DoesNotExist:
        mensaje = "Error, id no existe."

    productos = ProductoProveedor.objects.all()
    context = {
        'productos': productos,
        'mensaje': mensaje,
        'perfil': perfil,
        'platos': platos,
        'user_profile': user_profile,
    }
    return render(request, 'productos/productos_list.html', context)


def productos_findEdit(request, pk):
    perfil = request.session.get('perfil')
    platos = ProductoProveedor.objects.filter(stock__gt=0, disponibilidad=True)
    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    try:
        producto = ProductoProveedor.objects.get(id=pk)
        proveedores = Proveedor.objects.all()
        categorias = ProductoProveedor.CATEGORIAS  # Obtener las opciones de categoría desde el modelo

        context = {
            'producto': producto,
            'proveedores': proveedores,
            'categorias': categorias,  # Pasar las categorías al contexto
            'perfil': perfil,
            'platos': platos,
            'user_profile': user_profile,
        }
        return render(request, 'productos/productos_edit.html', context)
    except ProductoProveedor.DoesNotExist:
        context = {
            'mensaje': "Error, id no existe.",
            'perfil': perfil,
            'platos': platos,
            'user_profile': user_profile,
        }
        return render(request, 'productos/productos_list.html', context)


def productosUpdate(request):
    perfil = request.session.get('perfil')
    platos = ProductoProveedor.objects.filter(stock__gt=0, disponibilidad=True)
    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    if request.method == "POST":
        id_producto = request.POST.get("id")
        proveedor_id = request.POST.get("proveedor")
        nombre_producto = request.POST.get("nombre_producto")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        stock = request.POST.get("stock")
        disponibilidad = request.POST.get("disponibilidad")
        categoria = request.POST.get("categoria")
        imagen = request.FILES.get("imagen")  # Usar request.FILES para obtener archivos

        objProveedor = Proveedor.objects.get(id=proveedor_id)

        producto = ProductoProveedor.objects.get(id=id_producto)
        producto.proveedor = objProveedor
        producto.nombre_producto = nombre_producto
        producto.descripcion = descripcion
        producto.precio = precio
        producto.stock = stock
        producto.disponibilidad = disponibilidad
        producto.categoria = categoria
        if imagen:
            producto.imagen = imagen  # Actualizar la imagen solo si se proporcionó una nueva
        producto.save()
        producto.categoria = categoria
        producto.save()

        proveedores = Proveedor.objects.all()
        context = {
            'mensaje': "Datos actualizados",
            'proveedores': proveedores,
            'producto': producto,
            'perfil': perfil,
            'platos': platos,
            'user_profile': user_profile,
        }
        return render(request, 'productos/productos_edit.html', context)
    else:
        productos = ProductoProveedor.objects.all()
        context = {
            'productos': productos,
            'perfil': perfil,
            'platos': platos,
            'user_profile': user_profile,
        }
        return render(request, 'productos/productos_list.html', context)

def productos_categoria(request):
    productos_gatos = ProductoProveedor.objects.filter(categoria='comida_gatos')
    context = {'productos_gatos': productos_gatos}
    return render(request, 'productos/productos_categoria.html', context)


