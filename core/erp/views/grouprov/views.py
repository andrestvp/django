from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import GrouprovForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Grouprov


class GrouprovListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Grouprov
    template_name = 'grouprov/list.html'
    permission_required = 'view_grouprov'

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
                for i in Grouprov.objects.all():
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
        context['title'] = 'Listado de Grupo de Proveedores'
        context['create_url'] = reverse_lazy('erp:grouprov_create')
        context['list_url'] = reverse_lazy('erp:grouprov_list')
        context['entity'] = 'Grupo de Proveedores'
        return context


class GrouprovCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Grouprov
    form_class = GrouprovForm
    template_name = 'grouprov/create.html'
    success_url = reverse_lazy('erp:grouprov_list')
    permission_required = 'add_grouprov'
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
        context['title'] = 'Creación de Grupo de Proveedores'
        context['entity'] = 'Grupo de Proveedores'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class GrouprovUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Grouprov
    form_class = GrouprovForm
    template_name = 'grouprov/create.html'
    success_url = reverse_lazy('erp:grouprov_list')
    permission_required = 'change_grouprov'
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
        context['title'] = 'Edición de Grupo de Proveedores'
        context['entity'] = 'Grupo de Proveedores'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class GrouprovDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Grouprov
    template_name = 'grouprov/delete.html'
    success_url = reverse_lazy('erp:grouprov_list')
    permission_required = 'delete_grouprov'
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
        context['title'] = 'Eliminación de Grupo de Proveedores'
        context['entity'] = 'Grupo de Proveedores'
        context['list_url'] = self.success_url
        return context
