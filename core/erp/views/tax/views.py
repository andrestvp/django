from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import ImpuestoForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Impuesto


class TaxListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Impuesto
    template_name = 'tax/list.html'
    permission_required = 'view_tax'

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
                for i in Impuesto.objects.all():
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
        context['title'] = 'Impuestos'
        context['create_url'] = reverse_lazy('erp:tax_create')
        context['list_url'] = reverse_lazy('erp:tax_list')
        context['entity'] = 'Tax'
        return context


class TaxCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Impuesto
    form_class = ImpuestoForm
    template_name = 'tax/create.html'
    success_url = reverse_lazy('erp:tax_list')
    permission_required = 'add_category'
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
        context['title'] = 'Creación una Tax'
        context['entity'] = 'Tax'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TaxUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Impuesto
    form_class = ImpuestoForm
    template_name = 'tax/create.html'
    success_url = reverse_lazy('erp:tax_list')
    permission_required = 'change_tax'
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
        context['title'] = 'Edición una Tax'
        context['entity'] = 'Tax'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class TaxDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Impuesto
    template_name = 'tax/delete.html'
    success_url = reverse_lazy('erp:tax_list')
    permission_required = 'delete_tax'
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
        context['title'] = 'Eliminación de una Tax'
        context['entity'] = 'Taxs'
        context['list_url'] = self.success_url
        return context
