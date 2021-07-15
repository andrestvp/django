from django.contrib import admin
from core.erp.models import *
# Register your models here.
admin.site.register(Category)



class PurchaseAdmin(admin.ModelAdmin):
    list_display=(
        'cli',
        'subtotal',
        'state',
        'estado',

        


    )
    search_fields = ('cli',)



admin.site.register(Purchase, PurchaseAdmin)