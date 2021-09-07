import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView

from core.pos.forms import PurchaseForm, Purchase, PurchaseDetail, Product, Provider, DebtsPay, ProviderForm, PurchaseRequestForm
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class PurchaseRequestListView(PermissionMixin, FormView):
	model = PurchaseRequest
    template_name = 'scm/purchaserequest/list.html'
    permission_required = 'view_purchaserequest'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('purchaserequest_create')
        context['title'] = 'Solicitudes de Pedido'
        return context
#--------------------------------------------------------------------------------------------------------------------------------------------------------------


class PurchaseRequestCreateView(PermissionMIxin, CreateView):
	model=PurchaseRequest
	template_name = 'scm/purchaserequest/create.html'
	form_class=PurchaseRequestForm
	success_url = reverse_lazy('purchaserequest_list')
	permission_required = 'add_purchaserequest'
	
     def post(self, request, *args, **kwargs):
     	 action = request.POST['action']
     	 data = {}	
     	 try:
     	     if action == 'add':
     	     	 with transaction.atomic():
	     	     purchaserequest= PurchaseRequest()
	     	     purchaserequest.data_joined = request.POST['date_joined']
	     	     purchaserequest.save()
     	     
     	     	     for p in json.loads(request.POST['products']):
     	     	         prod = Product.objects.get(pk=p['id'])
     	     	         det = PurchaseRequestDetail()     	     
     	                 det = purchaserequest_id= purchaserequest.id
     	                 det.product_id = prod.id
     	                 det.cant= int(p['cant'])
     	                 det.cantitems=det.cantitems+int(det.cant) 
     	                 det.save()
     	          
     	                 det.product.stock += det.cant
                         det.product.save()
     	          
     	             purchaserequest.calculate_totalitems()
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
                    
             else:
             	data['error'] = 'No ha ingresado ninguna opcion'
      except Exception as e:
          data['error'] = str(e)
      return HttpsResponse(json.dumps(data), content_type='application/json')
      
      
   def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una solicitud'
        context['action'] = 'add'
        return context
        
#--------------------------------------------------------------------------------------------------------------------------------------------------
class PurchaseRequestDeleteView(PermissionMixin, DeleteView):
    model = PurchaseRequest
    template_name = 'scm/purchaserequest/delete.html'
    success_url = reverse_lazy('purchaserequest_list')
    permission_required = 'delete_purchaserequest'

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

        

          
      		       
            
                    
                    
     	       
     	          
     	               
     	          
     	          

	     	     
     	     
