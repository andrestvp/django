#from core.pos.models import Purchase
from core.pos.models import Sale
from django.contrib import admin
from core.pos.models import PurchaseRequest


# Register your models here.
#class SaleAdmin(admin.ModelAdmin):
#    list_display=(
#        'client',
#        'payment_condition',  
#        'sucursal',  
#        'plazo',
#        'estado',

#    )
#    search_fields = ('client',)

#admin.site.register(Sale, SaleAdmin)

class PurchaseRequestDetailAdmin(admin.ModelAdmin):
    list_display=(
        #'purchaserequest',
        'product',  
        'cant',  


    )
    search_fields = ('product',)




class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display=(
        #'purchaserequest',
        'reference',  
        'state',  


    )
    search_fields = ('state',)
admin.site.register(PurchaseRequest, PurchaseRequestAdmin)
#admin.site.register(Sale, SaleAdmin)

#class PurchaseAdmin(admin.ModelAdmin):
#    list_display=(
#            'provider',
#            'payment_condition',
#            'sucursal',
#            'state'
#)
#admin.site.register(Purchase, PurchaseAdmin)

#PurchaseDetail
#class PurchaseRequestAdmin(admin.ModelAdmin):
#    list_display=(
#        'reference',
#        'date_joined',  
#        'state',  


#    )
#    search_fields = ('reference',)

#admin.site.register(PurchaseRequestAdmin, PurchaseRequest)

