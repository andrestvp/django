#Importaciones de Modulos
from datetime import datetime
from django.db import models
from django.forms import model_to_dict
from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices, state_purchase, tipo_pago,ret_iva
from core.models import BaseModel
from django_fsm import FSMField, transition
from django_fsm_log.decorators import fsm_log_by, fsm_log_description

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']
#---------------------------------------------------------------------------------------------
class Sucursal(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    ubic = models.CharField(max_length=500, null=True, blank=True, verbose_name='Ubicación')

    def __str__(self):
        return self.ubic 

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursal'
        ordering = ['id']
#--------------------------------------------------------------------------------------
class SucursalDestino(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    ubic = models.CharField(max_length=500, null=True, blank=True, verbose_name='Ubicación de Destino')

    def __str__(self):
        return self.ubic

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'SucursalDestino'
        verbose_name_plural = 'SucursalDestino'
        ordering = ['id']

#--------------------------------------------------------------------------------------------------------------------

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    stock = models.IntegerField(default=2, verbose_name='Stock')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
    standardcost = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Costo Estándar')
    purchasecost = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Costo Compra')
    currentcost = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Costo Actual')
    datasheet = models.CharField(null=True, max_length=250, verbose_name='Ficha Técnica')
    detail = models.CharField(null=True, max_length=250, verbose_name='Detalle')
    maxstock = models.IntegerField(default=0, verbose_name='Stock Máximo')
    minstock = models.IntegerField(default=0, verbose_name='Stock Mínimo')
    suc = models.ForeignKey(Sucursal, on_delete=models.CASCADE, verbose_name='Sucursal' , null=True)
    codigo = models.CharField(null=True, max_length=150, verbose_name='Código', unique=True)
    

    #def __str__(self):
    #    return self.name


    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '[{}] {}'.format(self.codigo, self.name)



    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = '{} / {}'.format(self.name, self.cat.name)
        item['cat'] = self.cat.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        item['standardcost'] = format(self.standardcost, '.2f')

        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']
#-----------------------------------------------------------------------------------------

class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Cédula')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.names, self.surnames, self.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']

#-------------------------------------------------------------------------------------------------------------------------
class Tariff(models.Model):
    titulo = models.CharField(max_length=500, null=True, blank=True, verbose_name='Título', unique=True)
    dias = models.IntegerField( null=True, blank=True, verbose_name='Plazo de Pago')
    tipo = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tiempo Diferido')
    descuento = models.IntegerField( null=True, blank=True, verbose_name='Descuento Precio %')
    
    def __str__(self):
        return self.titulo

  
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tariff'
        verbose_name_plural = 'Tariff'
        ordering = ['id']
#----------------------------------------------------------------------------------------------------------------------------
class Grouprov(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Grouprov'
        verbose_name_plural = 'Grouprov'
        ordering = ['id']
#-----------------------------------------------------------------------------------------------------------------------------
class Provider(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Cédula')
    email = models.EmailField(max_length=30, unique=True, verbose_name='Correo')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    grupo = models.ForeignKey(Grouprov, on_delete=models.CASCADE, verbose_name='Grupo' , null=True)
    retencionesiva = models.CharField(max_length=10, choices=ret_iva, default=1, verbose_name='% Ret. IVA Bienes')
    retencionesservices = models.CharField(max_length=10, choices=ret_iva, default=1, verbose_name='% Ret. IVA Servicios')
    
    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.names, self.surnames, self.dni)

    def toJSON(self):
        item = model_to_dict(self)
        
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Provider'
        ordering = ['id']
#-------------------------------------------------------------------------------------------------------------------------------------------------

class Timelimit(models.Model):
    titulo = models.CharField(max_length=500, null=True, blank=True, verbose_name='Título', unique=True)
    dias = models.IntegerField( null=True, blank=True, verbose_name='Plazo de Pago')
    tipo = models.CharField(max_length=500, null=True, blank=True, verbose_name='Tiempo Diferido')
    
    
    def __str__(self):
        return self.titulo

    #def __str__(self):
    #    return self.get_titulo()

    #def get_titulo(self):
    #    return '{} {} '.format(self.dias, self.tipo)

    def toJSON(self):
        item = model_to_dict(self)
        return item



    #    item['full_titulo'] = self.get_titulo()


    class Meta:
        verbose_name = 'Timelimit'
        verbose_name_plural = 'Timelimit'
        ordering = ['id']


#---------------------------------------------------------------------------------------------------------------------------------------------------------------
class PriceList(models.Model):

    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Título') 
    dia = models.IntegerField( null=True, blank=True, verbose_name='Plazos de Pago')
    tiemp = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tiempo Diferido')
    desc = models.DecimalField(blank=True, default=0.00, max_digits=9, decimal_places=2, verbose_name='Descuento %')


    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'PriceList'
        verbose_name_plural = 'PriceList'
        ordering = ['id']

#--------------------------------------------------------------------------------------------------------------------------------------------------------
class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name="Subtotal 1")
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name="Subtotal 2")
    plazo = models.ForeignKey(PriceList, on_delete=models.CASCADE, null=True)
    entrada = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    totalpagar = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=tipo_pago, default='credito', verbose_name='Tipo de Pago')

    #ent = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        #item['plazo'] = self.plazo.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detsale_set.all():
            det.prod.stock += det.cant
            det.prod.save()
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']



#-------------------------------------------------------------------------------------------------------------------------------
class Payment(models.Model):
    name = models.CharField(max_length=150, verbose_name='Tipo de Pago', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['id']

#----------------------------------------------------------------------------------------------------------------------------------------------
class State(object):
    '''
    Constants to represent the `state`s of the PublishableModel
    '''
    INICIA = 'inicia'            # Early stages of content editing
    CREADA = 'creada'            # Early stages of content editing
    APROBADA = 'aprobada'      # Ready to be published
    PUBLICADA = 'publicada'    # Visible on the website
    CANCELADA = 'cancelada'        # Period for which the model is set to display has passed

    CHOICES = (
        (INICIA, INICIA),
        (CREADA, CREADA),
        (APROBADA, APROBADA),
        (PUBLICADA, PUBLICADA),
        (CANCELADA, CANCELADA),
    )



#-----------------------------------------------------------------------------------------------------------------------------------------------
class Impuesto(models.Model):
    name = models.CharField(max_length=150, verbose_name='Título', unique=True)
    valor = models.IntegerField( null=True, blank=True, verbose_name='Valor en %', unique=True)
    def __str__(self):
        return str(self.valor)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Impuesto'
        verbose_name_plural = 'Impuestos'
        ordering = ['id']
#-----------------------------------------------------------------------------------------------------------------------------------------------
class Purchase(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.CharField(max_length=10, choices=state_purchase, default='solicitud', verbose_name='Estado')
    plazo = models.ForeignKey(Timelimit, on_delete=models.CASCADE, null=True)
    tipo_pagos = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    tax = models.ForeignKey(Impuesto, on_delete=models.CASCADE, null=True)
    descuento = models.IntegerField(default=0,blank=True, verbose_name="Descuento")
    baseiva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True)
    #titulo = models.CharField(max_length=20, verbose_name='Plazo', null=True)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()   
        item['estado'] = {'estado': self.estado}
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detpurchase_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detpurchase_set.all():
            det.prod.stock += det.cant
            det.prod.save()
        super(Purchase, self).delete()

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchase'
        ordering = ['id']
#--------------------------------------------------------------------------------------------------------------
class DetPurchase(models.Model):
    sale = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Purchase'
        verbose_name_plural = 'Detalle de Purchase'
        ordering = ['id']

#----------------------------------------------------------------------------------------------------------------------
class PurchaseOrder(Purchase):
    class Meta:
        proxy = True

class Operaciones(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Operacion'
        verbose_name_plural = 'Operaciones'
        ordering = ['id']
#-----------------------------------------------------------------------------------------------------------------------
class Transfer(models.Model):
    Contacto = models.CharField(max_length=150, verbose_name='Responsable de envio')
    Operacion = models.ForeignKey(Operaciones, on_delete=models.CASCADE, verbose_name='Tipo de Operacion')
    sucorigen = models.ForeignKey(Sucursal, on_delete=models.CASCADE, verbose_name='Ubicacion de Origen')
    #sucodestino = models.ForeignKey(SucursalDestino, on_delete=models.CASCADE, verbose_name='Ubicacion de Destino')
    #sucdestino = models.ManytoManyField(Sucursal)
    fechaSalida = models.DateField(default=datetime.now, verbose_name='Fecha de Salida ')
    fechaPrevista = models.DateField(default=datetime.now, verbose_name='Fecha de Llegada')
    #docOrigin = models.CharField(max_lenght=150, verbose_name ='Nº Documento de Transferencia' )
    
    def __str__(self):
        return self.Contacto

    def toJSON(self):
        item = model_to_dict(self)
        item['Operacion'] = self.Operacion.toJSON()
        item['sucorigen'] = self.sucorigen.toJSON()
        item['det'] = [i.toJSON() for i in self.dettransfer_set.all()]

        return item


    def delete(self, using=None, keep_parents=False):
        for det in self.dettransfer_set.all():
            det.prod.stock -= det.cant
            det.prod.save()
        super(Transfer, self).delete()


    class Meta:
        verbose_name = 'Transfer'
        verbose_name_plural = 'Transfer'
        ordering = ['id']

#-----------------------------------------------------------------------------------------------------------------------------------------
class DetTransfer(models.Model):
    sale = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['transferencia'])
        item['prod'] = self.prod.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle de Transferencia'
        verbose_name_plural = 'Detalle de Transferencias'
        ordering = ['id']

#------------------------------------------------------------------------------------------------------------------------------------------
class Scrap(models.Model):

    name = models.ForeignKey(Product, on_delete=models.CASCADE)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Motivo')
    cant = models.IntegerField( null=True, blank=True, verbose_name='Cantidad')
    serie = models.IntegerField( null=True, blank=True, verbose_name='Serie')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Scrap'
        verbose_name_plural = 'Scrap'
        ordering = ['id']

#------------------------------------------------------------------------------------------------------------------------------
class Serie(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0, verbose_name='Cantidad')
    ref = models.CharField(max_length=150, verbose_name='Referencia', unique=True)
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha de creación')


    def __str__(self):
        return self.prod

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Serie'
        verbose_name_plural = 'Serie'
        ordering = ['id']
#-------------------------------------------------------------------------------------------------------------------------------
class Facturacion(models.Model):
    fechaemision = models.DateField(default=datetime.now, verbose_name='Fecha de Emision')
    serie = models.CharField(max_length=150, verbose_name='Serie', unique=True)
    concepto = models.CharField(max_length=150, verbose_name='Concepto', unique=True)
    cedula= models.CharField(max_length=150, verbose_name='Cedula', unique=True)
    codigo = models.CharField(max_length=150, verbose_name='Codigo', unique=True)
    fechavencimiento = models.CharField(max_length=150, verbose_name='Fecha de Vencimiento', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Facturacion'
        verbose_name_plural = 'Facturacion'
        ordering = ['id']
#-------------------------------------------------------------------------------------------------------------------------------
#class Quotations(Product, Client):
 #   numerocotizacion = models.CharField(max_length=150, verbose_name='Numero de Cotizacion', unique=True)
 #   codigo=models.ForeignKey(Product, verbose_name = 'Codigo', unique=True)
 #   cedula=models.ForeignKey(Client, verbose_name = 'C.I /RUC', unique=True)
 #   concepto=models.ForeignKey(Product, verbose_name = 'Concepto', unique=True)