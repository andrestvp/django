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

from core.erp.forms import SaleForm, ClientForm #,pedidosCompraForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import PriceList, Sale, Product, DetSale, Client, Timelimit, Vendor #PedidosCompra

#class PedidosCompraListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
#   model = PedidosCompra
#   template_name='solciitudCompra/list.html'
#   permission_required = 'view_PedidosCompra'
#   
#   @method_decorator(csrf_exempt)
#   def dispatch(self, request, *args, **kwargs):
#       return super().dispatch(request, *args, **kwargs)
#   
#   def post(self, request, *args, **kwargs)    
#       data = {}
#       try:
#           action=request.POST['action']
#           if action == 'searchdata':
#               data=[]
#               for i in PedidosCompra.objects.all()[0:500]:
#                   data.append(i.toJSON())
#           elif action == 'search_details_pedido':
#                data = []
#                for i in DetPedidoCompra.objects.filter(pedido_id=request.POST['id']):
#                       data.append(i.toJSON())
#           else:
#               data['error'] = 'Ha ocurrido un error'
#      except Exception  as e:
#           data['error'] = str(e)
#      return JsonResponse(data, safe=False)        
#   
#   def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['title'] = 'Solcitudes de Compra'
#        context['create_url'] = reverse_lazy('erp:solicitud_create')
#        context['list_url'] = reverse_lazy('erp:solicitud_list')
#        context['entity'] = 'Solicitudes'
#        return context   
#------------------------------------------------------------------------------------------------------------------------
#class PedidoCompraCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView)
#       model = PedidosCompra
#       form_class=PedidosCompraForm
#       template_name='solicitudCompra/create.html'
#       success_url=reverse_lazy('erp:solicitud_list')
#       permission_required = 'add_solicitud'
#       url_redirect = success_url
#     
#       @method_decorator(csrf_exempt)
#       def dispatch(self, request, *args, **kwargs):
#           return super().dispatch(request, *args, **kwargs)
#       
#       def post(self, *args, **kwargs):
#           data = {}
#           try:
#               action == request.POST['action']
#                if action == 'search_products':
#                    data = []
#                    ids_exclude = json.loads(request.POST['ids'])
#                    term=request.POST['term'].strip()
#                    products = Product.objects.filter(stock__gt=0)
#                    if len(term):
#                       products=products.filter(name_icontains=term)
#                    for i in products.exclude(id__in=ids_exclude)[0:10]:
#                        item=i.toJSON()
#                        item['value'] = i.name 
#                        data.append(item)
#                elif action == 'search_autocomplete':
#                   data = []
#                ids_exclude =json.loads(request.POST['ids'])
#                term=request.POST['term'].strip()
#                data.append({'id':term, 'text:term'})
#                products = Product.objects.filter(name__icontains=term, stock__gt=0)
#                for i in products.exclude(id__in=ids_exclude)[0:10]:
#                    item = 1.toJSON()
#                    item['text']=1.name                  
#                    data.append(item)
#               elif action == 'add':
#                  with transaction.atomic():
#                       solicitudes = json.loads(request.POST['solicitud'])                    
#                       pedido=PedidosCompra()
#                       pedido.data_joined=solicitud['data_joined']
#                       pedido.referencia=solicitud['referencia']
#
#    
#                for i in solicitud['solicitudes']:
#                   det = DetPedido()
#                   det.pedido_id=pedido.id
#                   det.producto_id=producto.id
#                   det.cantidad=int(i['cantidad'])
#                   det.costo=float(i['costo'])
#                   det.categoria_id=categoria.id
#                   det.referencia=i(['referencia'])    
#                   
#                   det.save()
#                   det.prod.save()
#               data={'id':pedido.id}
#
#                                   
#               else:
#                data['error'] = 'No ha ingresado a ninguna opción'
#        except Exception as e:
#            data['error'] = str(e)
#        return JsonResponse(data, safe=False)

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['title'] = 'Solicitud de Pedido'
#        context['entity'] = 'Solicitud de Pedido'
#        context['list_url'] = self.success_url
#        context['action'] = 'add'
#        context['det'] = []
#        return context
#
#------------------------------------------------------------------------------------------------------------------------
class PedidoCompraInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('solicitudCompra/solicitud.html')
            context = {
                'solicitud': PedidosCompra.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Créditos Palacios del Hogar', 'ruc': '9999999999999', 'address': 'Guayaquil'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:solicitud_list'))
