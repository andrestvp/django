from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import RecepcionCompraForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import RecepcionCompra


class RecepcionCompraListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = RecepcionCompra
    template_name = 'reception/list.html'
    permission_required = 'view_reception'

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
                for i in RecepcionCompra.objects.all():
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
        context['title'] = 'Listado de Recepcion Compra'
        context['create_url'] = reverse_lazy('erp:reception_create')
        context['list_url'] = reverse_lazy('erp:reception_list')
        context['entity'] = 'RecepcionCompra'
        return context


class RecepcionCompraCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = RecepcionCompra
    form_class = RecepcionCompraForm
    template_name = 'reception/create.html'
    success_url = reverse_lazy('erp:reception_list')
    permission_required = 'add_reception'
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
        context['title'] = 'Creación una RecepcionCompra'
        context['entity'] = 'RecepcionCompra'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class RecepcionCompraUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = RecepcionCompra
    form_class = RecepcionCompraForm
    template_name = 'reception/create.html'
    success_url = reverse_lazy('erp:reception_list')
    permission_required = 'change_reception'
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
        context['title'] = 'Edición una RecepcionCompra'
        context['entity'] = 'RecepcionCompra'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class RecepcionCompraDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = RecepcionCompra
    template_name = 'reception/delete.html'
    success_url = reverse_lazy('erp:reception_list')
    permission_required = 'delete_reception'
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
        context['title'] = 'Eliminación de una RecepcionCompra'
        context['entity'] = 'RecepcionCompra'
        context['list_url'] = self.success_url
        return context
