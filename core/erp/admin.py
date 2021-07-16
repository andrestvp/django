from django.contrib import admin
from core.erp.models import *
# Register your models here.
admin.site.register(Category)



class PurchaseAdmin(admin.ModelAdmin):
    list_display=(
        'cli',
        'subtotal',
        'estado',

        


    )
    search_fields = ('cli',)


class ClientAdmin(admin.ModelAdmin):
    list_display=(
        'names',
        'gender',
        'dni',

        


    )
    search_fields = ('cli',)

admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Client, ClientAdmin)