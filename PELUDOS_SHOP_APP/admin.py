from django.contrib import admin
from .models import *

 
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Proveedor)
admin.site.register(ProductoProveedor)
admin.site.register(Repartidores)
admin.site.register(DetalleCompra)

