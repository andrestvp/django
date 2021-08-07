from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import FinancieroPagosForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import FinancieroPagos


class FinancieroPagosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = FinancieroPagos
    template_name = 'financial/list.html'
    permission_required = 'view_financial'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in FinancieroPagos.objects.all():
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Pagos'
        context['create_url'] = reverse_lazy('erp:financial_create')
        context['list_url'] = reverse_lazy('erp:financial_list')
        context['entity'] = 'Categorias'
        return context


class FinancieroPagosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = FinancieroPagos
    form_class = FinancieroPagosForm
    template_name = 'financial/create.html'
    success_url = reverse_lazy('erp:financial_list')
    permission_required = 'add_financial'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación una Pagos'
        context['entity'] = 'Pagos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class FinancieroPagosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = FinancieroPagos
    form_class = FinancieroPagosForm
    template_name = 'financial/create.html'
    success_url = reverse_lazy('erp:financial_list')
    permission_required = 'change_financial'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Pagos'
        context['entity'] = 'Pagos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class FinancieroPagosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = FinancieroPagos
    template_name = 'financial/delete.html'
    success_url = reverse_lazy('erp:financial_list')
    permission_required = 'delete_financial'
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
        context['title'] = 'Eliminación de una Pagos'
        context['entity'] = 'Pagos'
        context['list_url'] = self.success_url
        return context
