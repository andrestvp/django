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


        


    )
    search_fields = ('cli',)



class ProductoAdmin(admin.ModelAdmin):
    list_display=(
        'name',
        'cat',
        'stock',
        'pvp',
        'costo',  


    )
    search_fields = ('name',)

class SaleAdmin(admin.ModelAdmin):
    list_display=(
        'cli',
        'plazo',
        'subtotal',
        'iva',
        'total',
        'entrada',
        'totalpagar',



    )
    search_fields = ('cli',)

admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Timelimit, TimeAdmin)
admin.site.register(DetPurchase, DetPurchaseAdmin)
admin.site.register(Product, ProductoAdmin)
admin.site.register(Sale, SaleAdmin)



