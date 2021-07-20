import random
from datetime import datetime

from django.db.models import Sum
from django.db.models.functions import Coalesce

from core.erp.models import Sale, DetSale
from core.erp.models import Purchase, DetPurchase


for m in range(0, 6):
    pedids = random.randint(18, 29)
    for d in range(1, pedids):
        vent = Sale()
        vent.cli_id = random.randint(1, 3)
        print('eeeeee',vent.cli_id)
        vent.date_joined = datetime(2020, m + 1, d)
        vent.save()

        food = random.randint(1, 10)

        for i in range(0, food):
            det = DetSale()
            det.sale_id = vent.id
            det.prod_id = random.randint(1, 23)
            det.price = det.prod.pvp
            det.cant = random.randint(1, 4)
            det.subtotal = float(det.price) * det.cant
            det.save()

        vent.subtotal = vent.detsale_set.all().aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
        vent.iva = float(vent.subtotal) * 0.12
        vent.total = float(vent.subtotal) + float(vent.iva)
        vent.save()
print('Terminado')


for m in range(0, 6):
    pedids = random.randint(18, 29)
    for d in range(1, pedids):
        vent = Purchase()
        vent.pla_id = random.randint(1, 3)
        print('xxx',vent.pla_id)
        vent.cli_id = random.randint(1, 3)
        print('eeeeee',vent.cli_id)
        vent.date_joined = datetime(2020, m + 1, d)
        vent.save()

        food = random.randint(1, 10)

        for i in range(0, food):
            det = DetPurchase()
            det.sale_id = vent.id
            det.prod_id = random.randint(1, 23)
            det.price = det.prod.pvp
            det.cant = random.randint(1, 4)
            det.subtotal = float(det.price) * det.cant
            det.save()

        vent.subtotal = vent.detpurchase_set.all().aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
        vent.iva = float(vent.subtotal) * 0.12
        vent.total = float(vent.subtotal) + float(vent.iva)
        vent.save()
print('Terminado')