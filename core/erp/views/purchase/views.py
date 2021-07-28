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
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from core.erp.forms import PurchaseForm, ClientForm, ProviderForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Purchase, Product, DetPurchase, Client, Timelimit, Provider


class PurchaseListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Purchase
    template_name = 'purchase/list.html'
    permission_required = 'view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Purchase.objects.all()[0:500]:
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetPurchase.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['create_url'] = reverse_lazy('erp:purchase_create')
        context['list_url'] = reverse_lazy('erp:purchase_list')
        context['entity'] = 'Compras'
        return context


class PurchaseCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'purchase/create.html'
    success_url = reverse_lazy('erp:purchase_list')
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
                    sale = Purchase()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    print('clii2',vents['cli'])
                    print('xxxxxy',vents['plazo'])
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.tipo_pagos_id = vents['tipo_pagos']
                    print('plaaa',sale.tipo_pagos_id)
                    sale.estado = "solicitud"
                    sale.plazo_id = vents['plazo']
                    print('plaaazx',sale.plazo_id)

                    #print('esb',sale.plazo)
                    #sale.plazo = sale.pla_id
                    #print('aaaa',sale.plazo)
                    #print('aaaab',sale.pla_id)

                    sale.save()
                    for i in vents['products']:
                        det = DetPurchase()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        det.prod.stock += det.cant
                        det.prod.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Provider.objects.filter(
                    Q(names__icontains=term) | Q(surnames__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = ProviderForm(request.POST)
                    data = frmClient.save()
            #elif action == 'search_plazo':
            #    data = []
            #    term = request.POST['term'].strip()
            #    plazo = Timelimit.objects.filter(
            #        Q(titulo__icontains=term) |Q(dias__icontains=term) | Q(tipo__icontains=term) )[0:10]
            #    for i in plazo:
            #        item = i.toJSON()
            #        item['text'] = i.titulo
            #        print('xxxxxxxxx',item['text'])
            #        data.append(item)
            elif action == 'create_correo':
                with transaction.atomic():
                    subject = request.POST.get('tema')
                    email=request.POST.get('email')
                    message = request.POST.get('message')

                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [email],
                    )                  
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Compras'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['frmClient'] = ProviderForm()
        return context


class PurchaseUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'purchase/create.html'
    success_url = reverse_lazy('erp:purchase_list')
    permission_required = 'change_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = PurchaseForm(instance=instance)
        form.fields['cli'].queryset = Provider.objects.filter(id=instance.cli.id)
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
                products = Product.objects.filter(name__icontains=term, stock__gt=0)
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
                    sale.plazo_id = vents['plazo']
                    sale.tipo_pagos_id = vents['tipo_pagos']

                    sale.estado = "aprobada"

                    sale.save()
                    sale.detpurchase_set.all().delete()
                    for i in vents['products']:
                        det = DetPurchase()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        det.prod.stock -= det.cant
                        det.prod.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Provider.objects.filter(
                    Q(names__icontains=term) | Q(surnames__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            
            elif action == 'search_plazo':
                data = []
                term = request.POST['term'].strip()
                plazo = Timelimit.objects.filter(
                    Q(titulo__icontains=term) |Q(dias__icontains=term) | Q(tipo__icontains=term) )[0:10]
                for i in plazo:
                    item = i.toJSON()
                    item['text'] = i.titulo
                    data.append(item)
            
            
            
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = ProviderForm(request.POST)
                    data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetPurchase.objects.filter(sale_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
        context['frmClient'] = ProviderForm()
        return context


class PurchaseDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Purchase
    template_name = 'purchase/delete.html'
    success_url = reverse_lazy('erp:purchase_list')
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
        context['title'] = 'Eliminación de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        return context


class PurchaseInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('purchase/invoice.html')
            context = {
                'sale': Purchase.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Creditos Palacio del Hogar .', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:purchase_list'))


