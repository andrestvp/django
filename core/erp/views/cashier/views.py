from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import CashierForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Cashier


class CashierListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Cashier
    template_name = 'cashier/list.html'
    permission_required = 'view_cashier'

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
                for i in Cashier.objects.all():
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
        context['title'] = 'Listado de Cajeros'
        context['create_url'] = reverse_lazy('erp:cashier_create')
        context['list_url'] = reverse_lazy('erp:cashier_list')
        context['entity'] = 'Cajero'
        return context


class CashierCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Cashier
    form_class = CashierForm
    template_name = 'cashier/create.html'
    success_url = reverse_lazy('erp:cashier_list')
    permission_required = 'add_cashier'
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
        context['title'] = 'Creación una cajero'
        context['entity'] = 'Cajero'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class CashierUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Cashier
    form_class = Cashier
    template_name = 'cashier/create.html'
    success_url = reverse_lazy('erp:cashier_list')
    permission_required = 'change_cashier'
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
        context['title'] = 'Edición una Cajero'
        context['entity'] = 'Cajero'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class CashierDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Cashier
    template_name = 'cashier/delete.html'
    success_url = reverse_lazy('erp:cashier_list')
    permission_required = 'delete_cashier'
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
        context['title'] = 'Eliminación de una Cajero'
        context['entity'] = 'Cajero'
        context['list_url'] = self.success_url
        return context
