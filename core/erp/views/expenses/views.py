from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import GastosForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Gastos


class GastosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Gastos
    template_name = 'expenses/list.html'
    permission_required = 'view_expenses'

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
                for i in Gastos.objects.all():
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
        context['title'] = 'Listado de Gastos'
        context['create_url'] = reverse_lazy('erp:expenses_create')
        context['list_url'] = reverse_lazy('erp:expenses_list')
        context['entity'] = 'Gastos'
        return context


class GastosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Gastos
    form_class = GastosForm
    template_name = 'expenses/create.html'
    success_url = reverse_lazy('erp:expenses_list')
    permission_required = 'add_expenses'
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
        context['title'] = 'Creación una Gastos'
        context['entity'] = 'Gastos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class GastosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Gastos
    form_class = GastosForm
    template_name = 'expenses/create.html'
    success_url = reverse_lazy('erp:expenses_list')
    permission_required = 'change_expenses'
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
        context['title'] = 'Edición una Gastos'
        context['entity'] = 'Gastos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class GastosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Gastos
    template_name = 'expenses/delete.html'
    success_url = reverse_lazy('erp:expenses_list')
    permission_required = 'delete_expenses'
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
        context['title'] = 'Eliminación de una Gastos'
        context['entity'] = 'Gastos'
        context['list_url'] = self.success_url
        return context
