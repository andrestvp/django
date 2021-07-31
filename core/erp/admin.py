from django.contrib import admin
from core.erp.models import *
# Register your models here.
admin.site.register(Category)




class ClientAdmin(admin.ModelAdmin):
    list_display=(
        'names',
        'gender',
        'dni',

        


    )
    search_fields = ('cli',)


class TimeAdmin(admin.ModelAdmin):
    list_display=(
        'titulo',
        'dias',
        'tipo',

        


    )
    search_fields = ('titulo',)

class DetPurchaseAdmin(admin.ModelAdmin):
    list_display=(
        'sale',
        'prod',
        'subtotal',
      

    )
    search_fields = ('sale',)



class PurchaseAdmin(admin.ModelAdmin):
    list_display=(
        'cli',
        'estado',
        'plazo',
        'tipo_pagos',


        


    )
    search_fields = ('cli',)



class ProductoAdmin(admin.ModelAdmin):
    list_display=(
        'name',
        'cat',
        'stock',
        'pvp',


    )
    search_fields = ('name',)

class SaleAdmin(admin.ModelAdmin):
    list_display=(
        'cli',
        'subtotal',
        'iva',
        'total',
        'entrada',
        'totalpagar',
        'tipo',
        'plazo',



        



    )
    search_fields = ('cli',)




class TransferAdmin(admin.ModelAdmin):
    list_display=(
        'Contacto',
        'Operacion',
        'sucorigen',
        'fechaPrevista',
        'fechaSalida',


        


    )
    search_fields = ('cli',)


class DetTransferAdmin(admin.ModelAdmin):
    list_display=(
        'sale',
        'prod',
        'cant',



        


    )
    search_fields = ('sale',)


class ImpuestoAdmin(admin.ModelAdmin):
    list_display=(
        'id',

        'name',
        'valor',    


    )
    search_fields = ('name',)
    


class ProviderAdmin(admin.ModelAdmin):
    list_display=(
        'names',
        'dni',

        


    )
    search_fields = ('names',)


class GrouprovAdmin(admin.ModelAdmin):
    list_display=(
        'name',
        'desc',

        


    )
    search_fields = ('name',)

class PriceListAdmin(admin.ModelAdmin):
    list_display=(
        'name',
        'desc',
   
    )
    search_fields = ('name',)

class FacturacionAdmin(admin.ModelAdmin):
    list_display=(
        'serie',
        'concepto',
   
    )
    search_fields = ('serie',)


#class PricesAdmin(admin.ModelAdmin):
#    list_display=(
#        'name',
#        'Porcentaje',
   
#    )
#    search_fields = ('name',)



admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Timelimit, TimeAdmin)
admin.site.register(DetPurchase, DetPurchaseAdmin)
admin.site.register(Product, ProductoAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(DetTransfer, DetTransferAdmin)
admin.site.register(Impuesto, ImpuestoAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Grouprov, GrouprovAdmin)
admin.site.register(PriceList, PriceListAdmin)
admin.site.register(Facturacion, FacturacionAdmin)
#admin.site.register(Prices, PricesAdmin)










