#from core.pos.models import Purchase
from core.pos.models import Sale
from django.contrib import admin

# Register your models here.
class SaleAdmin(admin.ModelAdmin):
    list_display=(
        'client',
        'payment_condition',  
        'sucursal',  
        'plazo',
        'estado',

    )
    search_fields = ('client',)

admin.site.register(Sale, SaleAdmin)

#class PurchaseAdmin(admin.ModelAdmin):
#    list_display=(
#            'provider',
#            'payment_condition',
#            'sucursal',
#            'state'
#)
#admin.site.register(Purchase, PurchaseAdmin)