import random
from datetime import datetime

from django.db.models import Sum
from django.db.models.functions import Coalesce

from core.erp.models import Sale, DetSale
from core.erp.models import Purchase, DetPurchase
from core.erp.models import Transfer, DetTransfer



for m in range(0, 6):
    pedids = random.randint(18, 29)
    for d in range(1, pedids):
        vent = Sale()
        vent.plazo_id = random.randint(1, 3)

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
        vent.plazo_id = random.randint(1, 3)
        print('xxx',vent.pla_id)
        vent.tipo_pagos_id = random.randint(1, 3)
        print('xxxz',vent.tipo_pagos_id)

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



for m in range(0, 6):
    pedids = random.randint(18, 29)
    for d in range(1, pedids):
        vent = Transfer()
        vent.Operacion_id = random.randint(1, 3)
        print('xxx',vent.Operacion_id)
        vent.sucorigen_id = random.randint(1, 3)
        print('xxxz',vent.sucorigen_id)


        vent.fechaSalida_id = datetime(2020, m + 1, d)
        vent.fechaPrevista_id = datetime(2020, m + 1, d)

        vent.save()

        food = random.randint(1, 10)

        for i in range(0, food):
            det = DetTransfer()
            det.sale_id = vent.id
            det.prod_id = random.randint(1, 23)
            det.price = det.prod.pvp
            det.cant = random.randint(1, 4)
            det.subtotal = float(det.price) * det.cant
            det.save()

        vent.subtotal = vent.dettransfer_set.all().aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
        vent.iva = float(vent.subtotal) * 0.12
        vent.total = float(vent.subtotal) + float(vent.iva)
        vent.save()
print('Terminado')