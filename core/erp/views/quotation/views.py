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

from core.erp.forms import SaleForm, ClientForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import PriceList, Sale, Product, DetSale, Client, Timelimit, Vendor

from decimal import Decimal

class QuotationSaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sale
    template_name = 'quotation/list.html'
    permission_required = 'view_quotation'

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
                for i in Sale.objects.filter(Q(estado='Cotización')| Q(estado='Cancelada') | Q(estado='Pedido'))[0:500]:
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
        context['title'] = 'Listado de Cotizaciones'
        context['create_url'] = reverse_lazy('erp:quotation_create')
        context['list_url'] = reverse_lazy('erp:quotation_list')
        context['entity'] = 'Cotizaciones'
        return context


class QuotationSaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'quotation/create.html'
    success_url = reverse_lazy('erp:quotation_list')
    permission_required = 'add_quotation'
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
                print("e crea")
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
                    sale.boispedido = (vents['boispedido'])
                    print('boispedido',(vents['boispedido']))
                    #sale.boisfactura = (vents['boisfactura'])

                    sale.entrada = float(vents['entrada'])
                    print('es',sale.entrada)
                    sale.tval = float(vents['tval'])
                    print('valdesc',sale.tval)
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
                        det.price = float(i['pvpchange'])
                        det.subtotal = float(i['subtotal'])
                        det.desc = float(i['desc'])

                        det.save()
                        #det.prod.stock -= det.cant
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
                    #print(data.append({'id':i.id, 'name':i.name}))



            elif action == 'search_pltipo':
                data = []
                for i in PriceList.objects.filter(tipo=request.POST['id']):
                    data.append({'id':i.id, 'name':i.name})
                    print(i.name)
                    #print(data.append({'id':i.id, 'name':i.name}))
                    #print(data.append({'id':i.id, 'name':i.name}))

            elif action == 'search_valor':
                print('entra a recorrer ra')
                data = []
                for i in PriceList.objects.filter(id=request.POST['id']):
                    print('entra a recorrer', i.desc)
                    #data.append({'id':i.id, 'name':i.desc})

                    data.append({'id':i.id,'desc':i.desc, 'name':i.name})



                    
                    #print(data.append({'id':i.id}))
                #term = request.POST['term']
                #print('entra a recorrer re')
                #pricel = PriceList.objects.filter(id=request.POST['id'])
                #print('entra a recorrer ri')
                #for i in pricel:
                #    print('entra a recorrer ro')
                #    item = i.toJSON()
                #    item['text'] = i.desc()
                #    print('eeennnn',item['text'])
                #    data.append(item)
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
        context['title'] = 'Creación de Cotización'
        context['entity'] = 'Cotización'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['frmClient'] = ClientForm()
        #context['ms']=Sale
        return context


class QuotationSaleUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'quotation/create.html'
    success_url = reverse_lazy('erp:quotation_list')
    permission_required = 'change_quotation'
    url_redirect = success_url

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
                print("e mod")
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # sale = Sale.objects.get(pk=self.get_object().id)
                    sale = self.get_object()
                    sale.date_joined = vents['date_joined']
                    print('date_joined',sale.date_joined)
                    sale.cli_id = vents['cli']
                    print('cli_id',sale.cli_id)
                    sale.subtotal = float(vents['subtotal'])
                    print('subtotal',sale.subtotal)
                    sale.iva = float(vents['iva'])
                    print('iva',sale.iva)
                    sale.total = float(vents['total'])
                    print('total',sale.total)
                    sale.boispedido = (vents['boispedido'])
                    print('boisp',sale.boispedido)
                    sale.boisfactura = (vents['boisfactura'])
                    print('boisfactura',sale.boisfactura)
                    sale.estado = (vents['estado'])
                    #print('estado asiig',sale.estado_id)
                    print('estado del otro lado',(vents['estado']))
                    print('estado del otro lado',sale.estado)

                    sale.entrada = float(vents['entrada'])
                    print('entrada',sale.entrada)
                    sale.tval = float(vents['tval'])
                    print('tval',sale.tval)
                    #sale.estado = "Facturación Completa"
                    sale.sucursal_id = vents['sucursal']
                    print('sucursal_id',sale.sucursal_id)
                    sale.vendedor_id = vents['vendedor']
                    print('vendedor_id',sale.vendedor_id)
                    sale.plazo_id = vents['plazo']
                    print('esbventa',sale.plazo_id)
                    sale.tipo = vents['tipo']
                    print('esbventa',sale.tipo)                                    
                    sale.totalpagar = float(vents['totalpagar'])
                    print('totalpagar',sale.totalpagar)
                    #sale.boisfactura = True
                    #if sale.boispedido == True:
                    #    if sale.boisfactura == False:
                    #        if sale.estado == "Cotización":
                    #            #sale.boisfactura = True
                    #            sale.estado= "Pedido"
                                #sale.boispedido = False
                    #            print('entra a cp',sale.estado)
                    #if sale.boisfactura == True:
                    #    if sale.boispedido == False:
                    #        if sale.estado == "Pedido":
                    #            sale.estado = "A Facturar"
                    #            print('enta a cf',sale.estado) 
                    sale.save()
                    sale.detsale_set.all().delete()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvpchange'])
                        det.subtotal = float(i['subtotal'])
                        det.desc = float(i['desc'])

                        det.save()
                        #det.prod.stock -= det.cant
                        det.prod.save()
                    data = {'id': sale.id}
         

            elif request.POST['submit']=='btnConfirmar':
                if 'btnConfirmar' in request.POST:
                    print('e brn')
            #elif action == 'search_status':
            #    print('entttttq')
            #    id = request.GET.get('id', False)

                #estado = request.GET.get('status', False)
                #id = request.Get.get('id',False)
                #job = Sale.objects.get(pk=id)
            #    job = Sale.objects.get(pk=id)

                #job.estado = "Pedido"
                #job.save()
            #    data = []
            #    for i in Sale.objects.filter(id=request.POST['id']):
            #        data.append({'id':i.id})
            #        print(i.id)

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
                    #print(data.append({'id':i.id, 'name':i.name}))



            elif action == 'search_pltipo':
                data = []
                for i in PriceList.objects.filter(tipo=request.POST['id']):
                    data.append({'id':i.id, 'name':i.name})
                    print(i.name)
                    #print(data.append({'id':i.id, 'name':i.name}))
                    #print(data.append({'id':i.id, 'name':i.name}))

            elif action == 'search_valor':
                print('entra a recorrer ra')
                data = []
                for i in PriceList.objects.filter(id=request.POST['id']):
                    print('entra a recorrer', i.desc)
                    #data.append({'id':i.id, 'name':i.desc})

                    data.append({'id':i.id,'desc':i.desc, 'name':i.name})

            elif action == 'search_estado':
                print('entra a recorrer ra')
                data = []
                for i in Sale.objects.filter(id=request.POST['id']):
                    print('entra a recorrer', i.desc)
                    #data.append({'id':i.id, 'name':i.desc})
                    print(i.estado)
                    data.append({'id':i.id,'estado':i.estado})
                    
                    #print(data.append({'id':i.id}))
                #term = request.POST['term']
                #print('entra a recorrer re')
                #pricel = PriceList.objects.filter(id=request.POST['id'])
                #print('entra a recorrer ri')
                #for i in pricel:
                #    print('entra a recorrer ro')
                #    item = i.toJSON()
                #    item['text'] = i.desc()
                #    print('eeennnn',item['text'])
                #    data.append(item)
            
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
    
    #class DecimalEncoder(json.JSONEncoder):
    #    def default(self, obj):
    #        if isinstance(obj, Decimal):
    #            return float(obj)
    #        return json.JSONEncoder.default(self, obj)


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
        print(self.object)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Cotización'
        context['entity'] = 'Cotización'
        context['list_url'] = self.success_url
        context['action']= 'edit'
        context['det'] = json.dumps(self.get_details_product())
        context['frmClient'] = ClientForm()
        return context


class QuotationSaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'quotation/delete.html'
    success_url = reverse_lazy('erp:quotation_list')
    permission_required = 'delete_quotation'
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
        context['title'] = 'Eliminación de Cotización'
        context['entity'] = 'Cotización'
        context['list_url'] = self.success_url
        return context


class QuotationSaleInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('quotation/invoice.html')
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
        return HttpResponseRedirect(reverse_lazy('erp:quotation_list'))



