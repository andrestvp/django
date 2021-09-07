from core.pos.models import Sale
from django.contrib import admin

# Register your models here.
class SaleAdmin(admin.ModelAdmin):
    list_display=(
        'client',
        'payment_condition',    

    )
    search_fields = ('client',)

admin.site.register(Sale, SaleAdmin)
