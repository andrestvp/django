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

from core.erp.forms import SaleForm, ClientForm, DetSalePaymentForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import PriceList, Sale, Product, DetSale, Client, Timelimit, Vendor


class ToInvoiceSaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sale
    template_name = 'toinvoice/list.html'
    permission_required = 'view_toinvoice'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                #for i in Sale.objects.all()[0:500]:
                for i in Sale.objects.filter(Q(estado='A Facturar'))[0:500]:
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de A Facturar'
        context['create_url'] = reverse_lazy('erp:toinvoice_create')
        context['list_url'] = reverse_lazy('erp:toinvoice_list')
        context['entity'] = 'A Facturar'
        return context


class ToInvoiceSaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'toinvoice/create.html'
    success_url = reverse_lazy('erp:toinvoice_list')
    permission_required = 'add_toinvoice'
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
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    print('es',sale.date_joined)

                    sale.cli_id = vents['cli']
                    print('es',sale.cli_id)

                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    print('total1',sale.total)

                    sale.entrada = float(vents['entrada'])
                    print('es',sale.entrada)
                    sale.estado = "Cotización"

                    sale.plazo_id = vents['plazo']
                    print('esbventa',sale.plazo_id)
                    sale.sucursal_id = vents['sucursal']
                    sale.vendedor_id = vents['vendedor']

                    sale.tipo = vents['tipo']
                    print('esbventat',sale.tipo)
                    sale.totalpagar = float(vents['totalpagar'])                
                    print('tt',sale.totalpagar)

                    sale.save()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.desc = float(i['desc'])

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
            elif action == 'search_vendor_id':
                data = []
                for i in Vendor.objects.filter(suc_id=request.POST['id']):
                    data.append({'id':i.id, 'name':i.name})
            elif action == 'search_valor':
                data = []
                for i in PriceList.objects.filter(desc_id=request.POST['id']):
                    print('entra a recorrer')
                    data.append({'id':i.id, 'name':i.desc}) 
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

            elif action == 'create_payment':
                print('entra pagov')
                with transaction.atomic():

                    #form2 = self.second_form_class(request.POST)
                    #if form2.is_valid():
                    #
                    frmFactura = DetSalePaymentForm(request.POST)
                    print('fr',frmFactura)
                    data = frmFactura.save()
                    print('df',data)


                    #pago = json.loads(request.POST['pago'])
                    #sale = Sale.objects.get(pk=self.get_object().id)
                    #sale = self.get_object()
                    #sale.tipofactura = pago['fechapago']
                    #print('ent paaag',sale.tipofactura)
                    #sale.fechapago = pago['fechapago']
                    #sale.total = float(pago['total'])
                    #sale.tipopagofact = (pago['tipopagofact'])
                    #sale.facturador_id = (pago['facturador'])
                    #sale.estado = (pago['estado'])
                    #sale.montodep = (pago['montodep'])
                    #sale.sucursal_id = vents['sucursal']
                    #sale.vendedor_id = vents['vendedor']
                    #sale.plazo_id = vents['plazo']
                    #print('esbventa',sale.plazo_id)
                    #sale.tipo_id = vents['tipo']
                    #print('esbventa',sale.tipo_id)
                    
                    

                    #sale.totalpagar = float(vents['totalpagar'])
                    #sale.save()




            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de A Facturar'
        context['entity'] = 'A Facturar'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['frmClient'] = ClientForm()
        context['frmFactura'] = DetSalePaymentForm()

        return context


class ToInvoiceSaleUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'toinvoice/create.html'
    success_url = reverse_lazy('erp:toinvoice_list')
    permission_required = 'change_toinvoice'
    url_redirect = success_url

    #second_form_class = DetSalePayment

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = SaleForm(instance=instance)
        form.fields['cli'].queryset = Client.objects.filter(id=instance.cli.id)
        return form

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
                products = Product.objects.filter(Q(name__icontains=term) | Q(codigo__icontains=term), stock__gt=0)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # sale = Sale.objects.get(pk=self.get_object().id)
                    sale = self.get_object()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.entrada = float(vents['entrada'])
                    sale.estado = "Facturación Completa"
                    sale.sucursal_id = vents['sucursal']
                    sale.vendedor_id = vents['vendedor']
                    sale.plazo_id = vents['plazo']
                    print('esbventa',sale.plazo_id)
                    sale.tipo_id = vents['tipo']
                    print('esbventa',sale.tipo_id)
                    
                    

                    sale.totalpagar = float(vents['totalpagar'])
                    sale.save()
                    sale.detsale_set.all().delete()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.desc = float(i['desc'])

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
                    print('cl',frmClient)
                    data = frmClient.save()
                    print('dt',data)

            elif action == 'create_payment':
                print('entra pagov')
                with transaction.atomic():

                    #form2 = self.second_form_class(request.POST)
                    #if form2.is_valid():
                    #
                    frmFactura = DetSalePaymentForm(request.POST)
                    print('fr',frmFactura)
                    data = frmFactura.save()
                    print('df',data)


                    #pago = json.loads(request.POST['pago'])
                    #sale = Sale.objects.get(pk=self.get_object().id)
                    #sale = self.get_object()
                    #sale.tipofactura = pago['fechapago']
                    #print('ent paaag',sale.tipofactura)
                    #sale.fechapago = pago['fechapago']
                    #sale.total = float(pago['total'])
                    #sale.tipopagofact = (pago['tipopagofact'])
                    #sale.facturador_id = (pago['facturador'])
                    #sale.estado = (pago['estado'])
                    #sale.montodep = (pago['montodep'])
                    #sale.sucursal_id = vents['sucursal']
                    #sale.vendedor_id = vents['vendedor']
                    #sale.plazo_id = vents['plazo']
                    #print('esbventa',sale.plazo_id)
                    #sale.tipo_id = vents['tipo']
                    #print('esbventa',sale.tipo_id)
                 
                  
                    #sale.totalpagar = float(vents['totalpagar'])
                    #sale.save()

                  
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                item['desc']= float(i.desc)

                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de A Facturar'
        context['entity'] = 'A Facturar'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
        context['frmClient'] = ClientForm()
        context['frmFactura'] = DetSalePaymentForm()
        #if 'form2' not in context:
        #    #context['form2']=self.second_form_class(self.request.GET)
        
        return context


class ToInvoiceSaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'toinvoice/delete.html'
    success_url = reverse_lazy('erp:toinvoice_list')
    permission_required = 'delete_toinvoice'
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
        context['title'] = 'Eliminación de A Facturar'
        context['entity'] = 'A Facturar'
        context['list_url'] = self.success_url
        return context


class ToInvoiceSaleInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('toinvoice/invoice.html')
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Créditos Palacios del Hogar', 'ruc': '9999999999999', 'address': 'Guayaquil'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:to_invoice_list'))
