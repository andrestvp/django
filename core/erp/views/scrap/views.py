from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import ScrapForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Scrap


class ScrapListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Scrap
    template_name = 'scrap/list.html'
    permission_required = 'view_scrap'

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
                for i in Scrap.objects.all():
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
        context['title'] = 'Listado Dar de Baja'
        context['create_url'] = reverse_lazy('erp:scrap_create')
        context['list_url'] = reverse_lazy('erp:scrap_list')
        context['entity'] = 'Dar de Baja'
        return context


class ScrapCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Scrap
    form_class = ScrapForm
    template_name = 'scrap/create.html'
    success_url = reverse_lazy('erp:scrap_list')
    permission_required = 'add_scrap'
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
        context['title'] = 'Creación Dar de Baja'
        context['entity'] = 'Dar de Baja'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ScrapUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Scrap
    form_class = ScrapForm
    template_name = 'scrap/create.html'
    success_url = reverse_lazy('erp:scrap_list')
    permission_required = 'change_scrap'
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
        context['title'] = 'Edición Dar de Baja'
        context['entity'] = 'Dar de Baja'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ScrapDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Scrap
    template_name = 'scrap/delete.html'
    success_url = reverse_lazy('erp:scrap_list')
    permission_required = 'delete_scrap'
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
        context['title'] = 'Eliminación de Dar de Baja'
        context['entity'] = 'Dar de Baja'
        context['list_url'] = self.success_url
        return context
