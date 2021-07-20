from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices, state_purchase
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

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
    costo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Costo')


    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = '{} / {}'.format(self.name, self.cat.name)
        item['cat'] = self.cat.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        item['costo'] = format(self.costo, '.2f')

        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

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

class Provider(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Cédula')
    email = models.EmailField(max_length=30, unique=True, verbose_name='Correo')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')

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

class Timelimit(models.Model):
    titulo = models.CharField(max_length=500, null=True, blank=True, verbose_name='Título')
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
        item['titulo'] = {'titulo': self.titulo}
        return item




    #    item['full_titulo'] = self.get_titulo()


    class Meta:
        verbose_name = 'Timelimit'
        verbose_name_plural = 'Timelimit'
        ordering = ['id']

class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
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


class Purchase(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.CharField(max_length=10, choices=state_purchase, default='solicitud', verbose_name='Estado')
    plazo = models.ForeignKey(Timelimit, on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=20, verbose_name='Plazo', null=True)

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





