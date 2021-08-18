from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import SecuencesForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Secuences


class SecuencesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Secuences
    template_name = 'secuences/list.html'
    permission_required = 'view_secuences'

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
                for i in Secuences.objects.all():
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
        context['title'] = 'Listado de Secuencias'
        context['create_url'] = reverse_lazy('erp:secuences_create')
        context['list_url'] = reverse_lazy('erp:secuences_list')
        context['entity'] = 'Secuencias'
        return context


class SecuencesCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Secuences
    form_class = SecuencesForm
    template_name = 'secuences/create.html'
    success_url = reverse_lazy('erp:secuences_list')
    permission_required = 'add_secuences'
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
        context['title'] = 'Creación Secuencias'
        context['entity'] = 'Secuencias'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class SecuencesUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Secuences
    form_class = SecuencesForm
    template_name = 'secuences/create.html'
    success_url = reverse_lazy('erp:secuences_list')
    permission_required = 'change_secuences'
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
        context['title'] = 'Edición Secuencias'
        context['entity'] = 'Secuencias'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class SecuencesDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Secuences
    template_name = 'category/delete.html'
    success_url = reverse_lazy('erp:secuences_list')
    permission_required = 'delete_secuences'
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
        context['title'] = 'Eliminación de Secuencias'
        context['entity'] = 'Secuencias'
        context['list_url'] = self.success_url
        return context
