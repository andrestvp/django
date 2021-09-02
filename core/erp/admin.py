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
        'ordencompra',
        'producto',
        'subtotal',
      

   )
    search_fields = ('ordencompra',)



#class PurchaseAdmin(admin.ModelAdmin):
#    list_display=(
#        'cli',
#        'estado',
#        'plazo',
#        'tipo_pagos',


        


#    )
#    search_fields = ('cli',)



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
        'tval',
        'iva',
        'total',
        'entrada',
        'totalpagar',
        'tipo',
        'plazo',
        'estado',
        'boispedido',
        'boisfactura'
     



    )
    search_fields = ('cli',)



    DetSale

class DetSaleAdmin(admin.ModelAdmin):
    list_display=(
        'sale',
        'prod',
        'price',
        'cant',
        'subtotal',
        'desc',



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
class SecuencesAdmin(admin.ModelAdmin):
    list_display=(
        'name',
        'suc',
   
    )
    search_fields = ('name',)

class SucursalAdmin(admin.ModelAdmin):
    list_display=(
        'name',
   
    )
    search_fields = ('name',)



class PedidosCompraAdmin(admin.ModelAdmin):
    list_display=(
        'referencia',
   
    )
    search_fields = ('referencia',)


class DetPedidoCompraAdmin(admin.ModelAdmin):
    list_display=(
        'pedido',
        'producto',
    )
    search_fields = ('pedido',)




class SaleRequestedAdmin(admin.ModelAdmin):
    list_display=(
        'cli',
        'subtotal',
        'tval',
        'iva',
        'total',
        'entrada',
        'totalpagar',
        'tipo',
        'plazo',
        'estado',
     



    )
    search_fields = ('cli',)



    

class DetSaleRequestedAdmin(admin.ModelAdmin):
    list_display=(
        'sale',
        'prod',
        'price',
        'cant',
        'subtotal',
        'desc',



    )
    search_fields = ('cli',)



class DetSalePaymentAdmin(admin.ModelAdmin):
    list_display=(
        'sale',
        'tipofactura',
        'fechapago',




    )
    search_fields = ('sale',)





#admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Timelimit, TimeAdmin)
#admin.site.register(DetPurchase, DetPurchaseAdmin)
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
admin.site.register(DetSale, DetSaleAdmin)
admin.site.register(Secuences, SecuencesAdmin)
admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(PedidosCompra, PedidosCompraAdmin)
admin.site.register(DetPedido, DetPedidoCompraAdmin)
admin.site.register(DetSaleRequested, DetSaleRequestedAdmin)
admin.site.register(SaleRequested, SaleRequestedAdmin)

admin.site.register(DetSalePayment, DetSalePaymentAdmin)













