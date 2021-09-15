import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, UpdateView

from core.pos.forms import PurchaseForm, Purchase,PurchaseRequestForm, PurchaseRequestDetail, PurchaseRequest, PurchaseOrder, PurchaseDetail,PurchaseOrderDetail, Product, Provider, DebtsPay, ProviderForm,PurchaseOrderForm
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class PurchaseOrderListView(PermissionMixin, FormView):
    template_name = 'scm/purchaseorder/list.html'
    permission_required = 'view_purchaseorder'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                search = PurchaseRequest.objects.filter()
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                for i in search:
                    data.append(i.toJSON())
            elif action == 'search_detproducts':
                print('entrali')
                data = []
                for det in PurchaseRequestDetail.objects.filter(purchaserequest_id=request.POST['id']):
                    data.append(det.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('purchaseorder_create')
        context['title'] = 'Listado de Ordenes'
        return context


class PurchaseOrderCreateView(PermissionMixin, CreateView):
    model = PurchaseRequest
    template_name = 'scm/purchaseorder/create.html'
    form_class = PurchaseRequestForm
    success_url = reverse_lazy('purchaseorder_list')
    permission_required = 'add_purchaseorder'

    def validate_provider(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Provider.objects.filter(name__iexact=obj):
                    data['valid'] = False
            elif type == 'ruc':
                if Provider.objects.filter(ruc__iexact=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if Provider.objects.filter(mobile=obj):
                    data['valid'] = False
            elif type == 'email':
                if Provider.objects.filter(email=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    purchaseorder = PurchaseRequest()
                    purchaseorder.provider_id = int(request.POST['provider'])
                    purchaseorder.payment_condition = request.POST['payment_condition']
                    purchaseorder.date_joined = request.POST['date_joined']
                    purchaseorder.reference = request.POST['reference']
                    purchaseorder.state = request.POST['state']
                    purchaseorder.concepto = request.POST['concepto']
                    purchaseorder.sucursal = request.POST['sucursal']

                    purchaseorder.save()

                    for p in json.loads(request.POST['products']):
                        prod = Product.objects.get(pk=p['id'])
                        det = PurchaseRequestDetail()
                        det.purchaseorder_id = purchaseorder.id
                        det.product_id = prod.id
                        det.cant = int(p['cant'])
                        det.price = float(p['price'])
                        det.subtotal = det.cant * float(det.price)
                        det.save()

                        det.product.stock += det.cant
                        det.product.save()

                    purchaseorder.calculate_invoice()

                    if purchaseorder.payment_condition == 'credito':
                        purchaseorder.end_credit = request.POST['end_credit']
                        purchaseorder.save()
                        debtspay = DebtsPay()
                        debtspay.purchaseorder_id = purchaseorder.id
                        debtspay.date_joinedorder = purchaseorder.date_joined
                        debtspay.end_date = purchaseorder.end_credit
                        debtspay.debt = purchaseorder.subtotal
                        debtspay.saldo = purchaseorder.subtotal
                        debtspay.save()
            elif action == 'search_products':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                search = Product.objects.filter(category__inventoried=True).exclude(id__in=ids).order_by('name')
                if len(term):
                    search = search.filter(name__icontains=term)
                    search = search[0:10]
                for p in search:
                    item = p.toJSON()
                    item['value'] = '{} / {}'.format(p.name, p.category.name)
                    data.append(item)
            elif action == 'search_provider':
                data = []
                for p in Provider.objects.filter(name__icontains=request.POST['term']).order_by('name')[0:10]:
                    item = p.toJSON()
                    item['text'] = '{} / {}'.format(p.name, p.ruc)
                    data.append(item)
            elif action == 'validate_provider':
                return self.validate_provider()
            elif action == 'create_provider':
                form = ProviderForm(request.POST)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['frmProvider'] = ProviderForm()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Orden de Compra'
        context['action'] = 'add'
        return context


class PurchaseOrderDeleteView(PermissionMixin, DeleteView):
    model = PurchaseOrder
    template_name = 'scm/purchaseorder/delete.html'
    success_url = reverse_lazy('purchaseorder_list')
    permission_required = 'delete_purchaseorder'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context



class PurchaseAdminUpdateView(PermissionMixin, UpdateView):
    model = PurchaseRequest    
    template_name = 'scm/purchaseorder/create.html'
    form_class = PurchaseRequestForm
    success_url = reverse_lazy('purchaseorder_list')
    permission_required = 'change_purchase'

    def validate_provider(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Provider.objects.filter(name__iexact=obj):
                    data['valid'] = False
            elif type == 'ruc':
                if Provider.objects.filter(ruc__iexact=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if Provider.objects.filter(mobile=obj):
                    data['valid'] = False
            elif type == 'email':
                if Provider.objects.filter(email=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = PurchaseRequestForm(instance=instance)
        #form.fields['client'].queryset = Client.objects.filter(id=instance.client.id)
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'edit':
                print('edit')
                with transaction.atomic():
                    #sale = Sale.objects.get(pk=self.get_object().id)
                    purchaserequest = self.get_object()
                    purchaserequest.date_joined = request.POST['date_joined']
                    purchaserequest.state = ''
                    purchaserequest.sucursal_id = request.POST['sucursal']
                  
                    purchaserequest.save()
                    purchaserequest.saledetail_set.all().delete()

                    for i in json.loads(request.POST['products']):
                        prod = Product.objects.get(pk=i['id'])
                        saledetail = PurchaseRequestDetail()
                        saledetail.purchaserequest_id = purchaserequest.id
                        saledetail.product_id = prod.id
                        saledetail.price = float(i['pvpchange'])
                        saledetail.cant = int(i['cant'])
                        saledetail.subtotal = saledetail.price * saledetail.cant
                        saledetail.dscto = float(i['dscto']) 
                        #saledetail.total_dscto = saledetail.dscto * saledetail.subtotal
                        saledetail.total = saledetail.subtotal
                        saledetail.save()

                        #saledetail.product.stock -= saledetail.cant
                        saledetail.product.save()

                    #purchaserequest.calculate_invoice()

                  
                       
                    data = {'id': purchaserequest.id}
            elif action == 'search_products':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                search = Product.objects.filter(category__inventoried=True).exclude(id__in=ids).order_by('name')
                if len(term):
                    search = search.filter(name__icontains=term)
                    search = search[0:10]
                for p in search:
                    item = p.toJSON()
                    item['value'] = '{} / {}'.format(p.name, p.category.name)
                    data.append(item)
            elif action == 'search_provider':
                data = []
                for p in Provider.objects.filter(name__icontains=request.POST['term']).order_by('name')[0:10]:
                    item = p.toJSON()
                    item['text'] = '{} / {}'.format(p.name, p.ruc)
                    data.append(item)
            elif action == 'validate_provider':
                return self.validate_provider()
            elif action == 'create_provider':
                form = ProviderForm(request.POST)
                data = form.save()          
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')


    def get_details_product(self):
        data=[]
        try:
            for i in PurchaseRequestDetail.objects.filter(purchaserequest_id=self.get_object().id):
                print('entra valor prod',i)
                item = i.product.toJSON()
                item['cant'] = i.cant
                print(item['cant'])
                item['dscto']= float(i.dscto)
                print(item)
                data.append(item)

        except:
            pass
        return data



    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['frmProvider'] = ProviderForm()

        context['title'] = 'Edición de una Orden de Compra'
        context['action'] = 'edit'
        #context['iva'] = Company.objects.first().get_iva()
        context['det'] = json.dumps(self.get_details_product())
        return context

