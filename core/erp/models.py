#Importaciones de Modulos
from datetime import datetime
from django.db import models
from django.forms import model_to_dict
from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices, state_purchase, tipo_pago,ret_iva,state_sale, Documentos, Tributo, Movimiento  #,#Cities
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

class Measures(models.Model):
    name = models.CharField(max_length=150, verbose_name = 'Medida', unique=True)
    type = models.CharField(max_length=150, verbose_name = 'Descripción Corta', unique=True)
    def __str__(self):
        return str(self.name)

    def toJSON(self):
        item = model_to_dict(self) 
        return item    
    class Meta:
        verbose_name = 'Medida'
        verbose_name_plural = 'Medidas'
        ordering = ['id']


#--------------------------------------------------------------------------------------------------------------------

class Product(models.Model):
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    stock = models.IntegerField(default=2, verbose_name='Stock')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
    standardcost = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Costo Estándar')
    #purchasecost = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Costo Compra')
    #currentcost = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Costo Actual')
    datasheet = models.CharField(null=True, max_length=250, verbose_name='Ficha Técnica')
    detail = models.CharField(null=True, max_length=250, verbose_name='Detalle')
    maxstock = models.IntegerField(default=0, verbose_name='Stock Máximo')
    minstock = models.IntegerField(default=0, verbose_name='Stock Mínimo')
    suc = models.ForeignKey(Sucursal, on_delete=models.CASCADE, verbose_name='Sucursal' , null=True)
    codigo = models.CharField(null=True, max_length=150, verbose_name='Código', unique=True)
    medidas = models.ForeignKey(Measures, on_delete=models.CASCADE, verbose_name='Medidas' , null=True)

    #imagesub = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')


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
#-----------------------------------------------------------------------------------------------
class Impuesto(models.Model):
    name = models.CharField(max_length=150, verbose_name='Título', unique=True)
    valor = models.IntegerField( null=True, blank=True, verbose_name='Valor en %', unique=True)

    def __str__(self):
        return str(self.valor)

    #@staticmethod
    #def get_default_valor():
    #    impuesto, created = Impuesto.objects.get_or_create(name = ' Default valor')
    #    return impuesto


    def get_default_valor(self):
        return str(self.valor)
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Impuesto'
        verbose_name_plural = 'Impuestos'
        ordering = ['id']




class Vendor(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    suc = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['suc'] = self.suc.toJSON()

        return item

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendor'
        ordering = ['id']


class Secuences(models.Model):
    name = models.CharField(max_length=150, verbose_name='Sucursal')
    emision = models.CharField(max_length=150, verbose_name='Pto. Emisión')
    numero = models.IntegerField(default=0, verbose_name='No. Actual')
    suc = models.ForeignKey(Sucursal, on_delete=models.CASCADE, verbose_name='Local' , null=True)

 
    
    def __str__(self):
        return self.get_full_secuences()

    def get_full_secuences(self):
        return '{} - {}'.format(self.name, self.emision)



    def toJSON(self):
        item = model_to_dict(self)

        item['suc']=self.suc.toJSON()
        return item
    
    class Meta:
        verbose_name = 'Secuencia'
        verbose_name_plural = 'Secuencias'
        ordering = ['id']






#--------------------------------------------------------------------------------------------------------------------------------------------------------
class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name="Subtotal 1")
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name="Subtotal 2")
    plazo = models.ForeignKey(PriceList, on_delete=models.CASCADE, null=True, blank=True)
    entrada = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    totalpagar = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=tipo_pago, verbose_name='Tipo de Pago', blank=False, null=False)
    tax = models.ForeignKey(Impuesto, on_delete=models.CASCADE, null=True, default=1)
    estado = models.CharField(max_length=10, choices=state_sale, default='Solicitud', verbose_name='Estado')
    vendedor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True)
    #femision = models.ForeignKey(Secuences, on_delete=models.CASCADE, null=True)


    #ent = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    #def save(self, *args, **kwargs):
    #    if self.tax is None:
    #        self.tax = Impuesto.get_default_params()

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        #item['plazo'] = self.plazo.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['totalpagar'] = format(self.totalpagar, '.2f')
        item['entrada'] = format(self.entrada, '.2f')

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
    desc = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['desc'] = format(self.desc, '.2f')

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

#-----------------------------------------------------------------------------------------------------------------------------------------------
class Purchase(models.Model):
    cli = models.ForeignKey(Provider, on_delete=models.CASCADE)
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
    #sucodestino = models.ForeignKey(SucursalDestino, on_delete=models.CASCADE, verbose_name='Ubicacion de Destino')
    #sucdestino = models.ManytoManyField(Sucursal)
    fechaSalida = models.DateField(default=datetime.now, verbose_name='Fecha de Salida ')
    fechaPrevista = models.DateField(default=datetime.now, verbose_name='Fecha de Llegada')
    concepto = models.CharField(max_length=150, verbose_name='Concepto', null=True, blank=True)
    observacion = models.CharField(max_length=150, verbose_name='Observación', null=True, blank=True,)
    referencia = models.CharField(max_length=150, verbose_name='Referencia', null=True, blank=True,)
    #docOrigin = models.CharField(max_lenght=150, verbose_name ='Nº Documento de Transferencia' )
    sucorigen = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="sucorigen_fixturetables")
    sucdestino = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="sucdestino_fixturetables")

#team_one = models.ForeignKey(Team, related_name="team_one_fixturetables")
#team_two = models.ForeignKey(Team, related_name="team_two_fixturetables")

    #sucdestino = models.ForeignKey(SucursalDestino, on_delete=models.CASCADE, verbose_name='Ubicacion de destino', blank=True)

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
    fechavencimiento = models.DateField(default=datetime.now, verbose_name='Fecha de Vencimiento')

    def __str__(self):
        return self.concepto

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Facturacion'
        verbose_name_plural = 'Facturacion'
        ordering = ['id']
#-------------------------------------------------------------------------------------------------------------------------------
#class Quotations(models.Model):
 #   numerocotizacion = models.PositiveIntegerField(max_length=150, verbose_name='Numero de Cotizacion', unique=True)
 #   codigo=models.ForeignKey(Product, verbose_name = 'Codigo', unique=True)
 #   cedula=models.ForeignKey(Client, verbose_name = 'C.I /RUC', unique=True)
 #   detail=models.ForeignKey(Product, verbose_name = 'Concepto' unique=True)
 #   name=models.ForeignKey(Vendor, verbose_name='Vendedor' unique=True)
 #


 #------------------------------------------------------------------------------------------------------------------------------

 #class Facturador(Model.Models):
 #------------------------------------------------------------------------------------------------------------------------------

class Prices(models.Model):
    name = models.CharField(max_length=150, verbose_name='Título', unique=True)
    Porcentaje = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Tarifa en %')

    def __str__(self):
        return str(self.name)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Precio'
        verbose_name_plural = 'Precios'
        ordering = ['id']
 #--------------------------------------------------------------------------------------------------------------------------------------    

 #------------------------------------------------------------------------------------------------------------

 #-----------------------------------------------------------------------------------------------------------
class CreditCard(models.Model):
    description=models.CharField(max_length=150, verbose_name='Descripcion', unique=True)
    
    def __str__(self):
        return str(self.description)

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta: 
        verbose_name = 'Tarjeta'
        verbose_name_plural = 'Tarjetas'  
        ordering = ['id']  
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------        
#---------------------------------------------------------------------------------------------------------------------------
class RecepcionCompra(models.Model):
    nrecepcion = models.PositiveIntegerField( null=True, blank=True, verbose_name='Secuencia', unique=True)
    proveedor=models.ForeignKey(Provider, on_delete=models.CASCADE, null = True)
    concepto=models.CharField(max_length=150, verbose_name='Concepto', unique=True)
    fecha=models.DateTimeField(default=datetime.now)
    codigo=models.CharField(max_length=150, verbose_name='codigo')
    almacen = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True)
    costos = models.ForeignKey(Tariff, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.nrecepcion)

    def toJSON(self):
        item = model_to_dict(self)
        return item
   
    class Meta:
        verbose_name = 'Recepciones de Compra'
        verbose_name_plural= 'Recepciones de Compras'
        ordering = ['id']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
   
#------------------------------------------------------------------------------------------------------------------------------
# class BasicInfo(models.Model):
#   creada=models.DatetimeField(auto_now_add=True)
#   class Meta:
#       abstract = True
#-----------------------------------------------------------------------------------------------------------------------------

#class Services(models.Model):
#   
#------------------------------------------------------------------------------------------------------------------------------
class PlanCuentas(models.Model):
    codigocontable=models.CharField(max_length=150, verbose_name='Concepto', unique=True)
    descripcion=models.TextField(max_length=150, verbose_name='Descripcion', unique=True)
    
    def __str__(self):
        return str(self.descripcion)

    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        verbose_name = 'Plan de Cuenta'
        verbose_name_plural= 'Planes de Cuentas'
        ordering = ['id']   
#-------------------------------------------------------------------------------------------------------------------------------
class Gastos(models.Model): 
    cuenta=models.ForeignKey(PlanCuentas, on_delete =models.CASCADE)
    retenciones = models.CharField(max_length=10, choices=ret_iva, default=1, verbose_name='Retenciones')
    iva=models.ForeignKey(Impuesto, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.cuenta)
   
    def toJSON(self):
        item = model_to_dict(self)
        item['cuenta'] = self.cuenta.toJSON()
        item['iva'] = self.iva.toJSON()

       
        return item
   
    class Meta:
        verbose_name = 'Gastos'
        verbose_name_plural= 'Gastos'
        ordering = ['id']   


#--------------------------------------------------------------------------------------------------------------------------------
#class EstadoGastos(models.Model):
#    estado = models.CharField(max_length=10, choices=EstadoGastos, default=1, verbose_name='Estado de Gastos')
#    def__str__(self):
#        return self.estado
#   class Meta:
#       abstract = True
#----------------------------------------------------------------------------------------------------------------------------------
class Compras(models.Model):

    cli = models.ForeignKey(Provider, on_delete=models.CASCADE)
    secuenceValue = models.PositiveIntegerField( null=True, blank=True, verbose_name='Secuencia', unique=True)
    femision=models.DateTimeField(default=datetime.now)
    fregistro=models.DateTimeField(default=datetime.now)
    concepto=models.CharField(max_length=150, verbose_name='Concepto', unique=True)
    codigo=models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    tipoDocumento = models.CharField(max_length=10, choices=Documentos, default=1, verbose_name='Documentos')
    autorizacion=models.PositiveIntegerField( null=True, blank=True, verbose_name='Autorizacion', unique=True)
    sustributario = models.CharField(max_length=10, choices=Tributo, default= 1 ,verbose_name='Tributos')
    sucursal=models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.CharField(max_length=10, choices=state_purchase, default='solicitud', verbose_name='Estado')
    plazo = models.ForeignKey(Timelimit, on_delete=models.CASCADE, null=True)
    tipo_pagos = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    tax = models.ForeignKey(Impuesto, on_delete=models.CASCADE, null=True)
    descuento = models.IntegerField(default=0,blank=True, verbose_name="Descuento")
    baseiva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
   
    def __str__(self):
        return self.cli.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()   
        item['estado'] = {'estado': self.estado}
        item['subtotal'] = format(self.subtotal, '.2f')
        item['tax'] = self.tax.toJSON()   
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
#
#
#
# ---------------------------------------------------------------------------------
class PurchaseOrderOficial(models.Model):

    cli=models.ForeignKey(Provider,on_delete=models.CASCADE)
    date_joined=models.DateTimeField(default=datetime.now)
    referencia=models.CharField(max_length=150, verbose_name='Referencia', unique=True)
    concepto=models.CharField(max_length=150, verbose_name='Concepto', unique=True)
    codigo=models.CharField(max_length=150,verbose_name='codigo', unique=True)
    suscursal=models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True)
    costo=models.ForeignKey(Tariff, on_delete=models.CASCADE, null=True)
    autorizacion=models.PositiveIntegerField( null=True, blank=True, verbose_name='Autorizacion', unique=True)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    descuento = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.CharField(max_length=10, choices=state_purchase, default ='solicitud', verbose_name='Estado')
    plazo = models.ForeignKey(Timelimit, on_delete=models.CASCADE, null=True)
    tipo_pagos = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    tax = models.ForeignKey(Impuesto, on_delete=models.CASCADE, null=True)
    baseiva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantitems = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)


    def __str__(self):
        return self.cli.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()   
        item['estado'] = {'estado': self.estado}
        item['subtotal'] = format(self.subtotal, '.2f')
        item['tax'] = self.tax.toJSON()   
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        #item['det'] = [i.toJSON() for i in self.detpurchase_set.all()]
        return item

    #def delete(self, using=None, keep_parents=False):
    #    for det in self.detpurchase_set.all():
    #        det.prod.stock += det.cant
    #        det.prod.save()
    #    super(Purchase, self).delete()

    class Meta:
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Ordenes de Compra'
        ordering = ['id']

#-----------------------------------------------------------------------------------------------------------------------------------
class FinancieroPagos(models.Model):
    cli = models.ForeignKey(Provider, on_delete=models.CASCADE)
    codigoPago=models.CharField(max_length=150, verbose_name='Codigo', unique=True)
    femision=models.DateTimeField(default=datetime.now)
    fvencimiento=models.DateTimeField(default=datetime.now)
    concepto=models.CharField(max_length=150, verbose_name='Concepto', unique=True)
    movimiento = models.CharField(max_length=10, choices=Movimiento, default='Saldo Inicial Pagos', verbose_name='Movimiento')
    valorDeuda = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Valor Deuda')
    
    def __str__(self):
        return str(self.codigoPago)

    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        verbose_name = 'Pago Proveedores'
        verbose_name_plural= 'Pago Proveedores'
        ordering = ['id']     
 
# --------------------------------------------------------------------------------------------------------------------------------