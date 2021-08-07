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

from core.erp.forms import TransferForm, ClientForm, PurchaseOrderForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Transfer, Product, DetTransfer, Client, Timelimit, PurchaseOrder


class purchaseOrderListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = PurchaseOrder
    template_name = 'purchaseOrder/list.html'
    permission_required = 'view_transfer'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Transfer.objects.all()[0:500]:
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetTransfer.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Solicitudes de Compra'
        context['create_url'] = reverse_lazy('erp:purchaseOrder_create')
        context['list_url'] = reverse_lazy('erp:purchaseOrder_list')
        context['entity'] = 'purchaseOrder'
        return context


class purchaseOrderCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = PurchaseOrder
    form_class =  PurchaseOrderForm
    template_name = 'purchaseOrder/create.html'
    success_url = reverse_lazy('erp:purchaseOrder_list')
    permission_required = 'add_sale'
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
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Transfer()
                    sale.fechaSalida_id = vents['fechaSalida']
                    sale.Contacto = vents['Contacto']
                    print('eeesa',sale.Contacto)
                    sale.Operacion_id = vents['Operacion']
                    sale.sucorigen_id = vents['sucorigen']
                    sale.fechaPrevista_id = vents['fechaPrevista']                   
                    print('es',sale.fechaPrevista)
             

                    sale.save()
                    for i in vents['products']:
                        det = DetTransfer()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])

                        det.save()
                        det.prod.stock -= det.cant
                        det.prod.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(
                    Q(names__icontains=term) | Q(surnames__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in clients:
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
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = ClientForm(request.POST)
                    data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una orden de Compra'
        context['entity'] = 'purchaseOrder'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['frmClient'] = ClientForm()
        return context


class purchaseOrderUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchaseOrder/create.html'
    success_url = reverse_lazy('erp:purchaseOrder_list')
    permission_required = 'change_sale'
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
                    vents = json.loads(request.POST['vents'])
                    sale = Transfer()
                    sale.fechaSalida_id = vents['fechaSalida']
                    sale.Contacto = vents['Contacto']
                    print('eeesaf',sale.fechaSalida_id)
                    sale.Operacion_id = vents['Operacion']
                    sale.sucorigen_id = vents['sucorigen']
                    sale.fechaPrevista_id = vents['fechaPrevista']                    
                    print('esf',sale.fechaPrevista_id)
                    sale.save()
                    sale.dettransfer_set.all().delete()
                    for i in vents['products']:
                        det = DetTransfer()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.save()
                        det.prod.stock -= det.cant
                        det.prod.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(
                    Q(names__icontains=term) | Q(surnames__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in clients:
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
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = ClientForm(request.POST)
                    data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetTransfer.objects.filter(sale_id=self.get_object().id):
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
        context['frmClient'] = ClientForm()
        return context


class purchaseOrderDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = PurchaseOrder
    template_name = 'purchaseOrder/delete.html'
    success_url = reverse_lazy('erp:purchaseOrder_list')
    permission_required = 'delete_sale'
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
                'sale': PurchaseOrder.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Credito Palacios del Hogar S.A.', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:purchaseOrder_list'))
