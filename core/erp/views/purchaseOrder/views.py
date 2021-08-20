import json
import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from weasyprint import HTML, CSS

from core.erp.forms import TransferForm, ClientForm, PurchaseOrderOficialForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import *

#-----------------------------------------------------------------------------------
class PurchaseOrderOficialListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = PurchaseOrderOficial
    template_name = 'purchaseOrder/list.html'
    permission_required = 'view_PurchaseOrderOficial'
#
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data=[]
                for i in purchaseOrderOficial.objects.all()[0:500]:
                    data.append(i.toJSON())
            elif  action == 'search_details_prod':
             data = []
             for i in DetPurchaseOrder.objects.filter(ordencompra_id=request.POST['id']):
                 data.append(i.toJSON())
            else:
               data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ordenes de Compra'
        context['create_url'] = reverse_lazy('erp:purchaseOrder_create')
        context['list_url'] = reverse_lazy('erp:purchaseOrder_list')
        context['entity'] = 'PurchaseOrderOficial'
        return context

class purchaseOrderOficialCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = PurchaseOrderOficial
    form_class =  PurchaseOrderOficialForm
    template_name = 'purchaseOrder/create.html'
    success_url = reverse_lazy('erp:purchaseOrder_list')
    permission_required = 'add_PurchaseOrderOficial'
    url_redirect = success_url
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter(stock__gt=0)
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.name
                    # item['text'] = i.name
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(Q(name__icontains=term) | Q(codigo__icontains=term) , stock__gt=0)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    ordenes = json.loads(request.POST['ordenes'])
                    ordencompra = PurchaseOrderOficial()
                    ordencompra.date_joined = ordenes['date_joined']
                    ordencompra.cli_id=ordenes['cli']
                    ordencompra.referencia = ordenes['referencia']
                    ordencompra.suscursal_id = ordenes['sucursal']
                    ordencompra.tipo_pagos = ordenes['tipo_pagos'] 
                    ordencompra.plazo_id=ordenes['plazo']    
                    ordenCompra.tax_id=ordenes['tax']
                    ordencompra.subtotal=float(ordenes['subtotal'])
                    ordencompra.abono=ordenes['abono']
                    ordencompra.estado= "Aprobado"
                    ordencompra.iva=float(['iva'])
                    ordencompra.total=float(['total'])

                    ordencompra.save()
                    for i in ordenes['products']:
                        det = DetPurchaseOrder()
                        det.cli_id = cli.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cant'])
                        det.costo=float(i['costo'])
                        det.subtotal = float(i['subtotal'])
                        det.desc = float(i['desc'])
                        det.save()
                        det.producto.stock += det.cant
                        det.producto.save()
                    data = {'id': sale.id}
            elif action == 'search_providers':
                data = []
                term = request.POST['term']
                providers = Provider.objects.filter(
                    Q(names__icontains=term) | Q(surnames__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in providers:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            #elif action == 'search_plazo':
            #    data = []
            #    term = request.POST['term'].strip()
            #    plazo = Timelimit.objects.filter(
            #        Q(titulo__icontains=term) |Q(dias__icontains=term) | Q(tipo__icontains=term) )[0:10]
            #    for i in plazo:
            #        item = i.toJSON()
            #        item['text'] = i.titulo
            #        print('zzzz',item['text'])
            #        data.append(item)
            elif action == 'create_provider':
                with transaction.atomic():
                    frmProvider = ProviderForm(request.POST)
                    data = frmProvider.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una orden de Compra'
        context['entity'] = 'purchaseOrderOficial'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['frmProvider'] = ProviderForm()
        return context


class purchaseOrderOficialUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = PurchaseOrderOficial
    form_class = PurchaseOrderOficialForm
    template_name = 'purchaseOrder/create.html'
    success_url = reverse_lazy('erp:purchaseOrder_list')
    permission_required = 'change_purchaseOrder'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter(stock__gt=0)
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.name
                    # item['text'] = i.name
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(name__icontains=term, stock__gt=0)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    ordenes = json.loads(request.POST['ordenes'])
                    ordenCompra = PurchaseOrderOficial()
                    ordenCompra.date_joined = ordenes['date_joined']
                    ordenCompra.cli_id=ordenes['cli']
                    ordenCompra.referencia = ordenes['referencia']
                    ordenCompra.suscursal_id = ordenes['sucursal']
                    ordenCompra.costo = float(ordenes['ordenes'])
                    ordenCompra.tipo_pagos_id = ordenes['tipo_pagos'] 
                    ordenCompra.plazo_id=ordenes['plazo']    
                    ordenCompra.tax_id=ordenes['tax']
                    ordenCompra.subtotal=float(ordenes['subtotal'])
                    ordenCompra.baseiva=ordenes['baseiva']
                    ordenCompra.estado= 'solicitud'
                    ordenCompra.iva=float(['iva'])
                    ordenCompra.total=float(['total'])
                    ordenCompra.cantitems=int(['cantitems'])
                    ordenCompra.save()
                    sale.dettransfer_set.all().delete()
                    for i in ordenes['products']:
                        det = DetPurchaseOrder()()
                        det.referencia_id = referencia.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.save()
                        det.producto.stock += det.cantidad
                        det.producto.save()
                    data = {'id': sale.id}
            elif action == 'search_providers':
                data = []
                term = request.POST['term']
                providers = Provider.objects.filter(
                    Q(names__icontains=term) | Q(surnames__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in providers:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            #elif action == 'search_plazo':
            #    data = []
            #    term = request.POST['term'].strip()
            #    plazo = Timelimit.objects.filter(
            #        Q(titulo__icontains=term) |Q(dias__icontains=term) | Q(tipo__icontains=term) )[0:10]
            #    for i in plazo:
            #        item = i.toJSON()
            #        item['text'] = i.titulo
            #        print('zzzz',item['text'])
            #        data.append(item)
            elif action == 'create_provider':
                with transaction.atomic():
                    frmProvider = ProviderForm(request.POST)
                    data = frmProvider.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetpurchaseOrder.objects.filter(referencia_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Orden de Compra'
        context['entity'] = 'purchaseOrder'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
        context['frmProvider'] = ProviderForm()
        return context


class purchaseOrderDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = PurchaseOrderOficial
    template_name = 'purchaseOrder/delete.html'
    success_url = reverse_lazy('erp:purchaseOrder_list')
    permission_required = 'delete_purchaseOrder'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Orden de Compra'
        context['entity'] = 'purchaseOrder'
        context['list_url'] = self.success_url
        return context


class purchaseOrderPdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('purchaseOrder/purchaseOrder.html')
            context = {
                'orden': PurchaseOrder.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Credito Palacios del Hogar S.A.', 'ruc': '9999999999999', 'address': 'Guayaquil, Ecuador'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, bsase_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:purchaseOrder_list'))
