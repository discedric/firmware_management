import logging
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.template import Template
from netbox.views import generic
from utilities.query import count_related
from utilities.views import register_model_view, ViewTab

from ..utils import get_countdevice
from .. import tables
from .. import forms
from .. import models
from .. import filtersets

__all__ = (
    'FirmwareView',
    'FirmwareListView',
    'FirmwareChangeLogView',
    'FirmwareJournalView',
)

@register_model_view(models.Firmware)
class FirmwareView(generic.ObjectView):
    queryset = models.Firmware.objects.all()

    def get_extra_context(self, request, instance):
        context = super().get_extra_context(request, instance)
        return context

class FirmwareChangeLogView(generic.ObjectChangeLogView):
    """View for displaying the changelog of a Firmware object"""
    queryset = models.Firmware.objects.all()
    model = models.Firmware
    
    def get(self, request, pk):
        return super().get(request, pk=pk, model=self.model)

class FirmwareJournalView(generic.ObjectJournalView):
    """View for displaying the journal of a Firmware object"""
    queryset = models.Firmware.objects.all()
    model = models.Firmware
    
    def get(self, request, pk):
        return super().get(request, pk=pk, model=self.model)

@register_model_view(models.Firmware, 'list', path='', detail=False)
class FirmwareListView(generic.ObjectListView):
    queryset = models.Firmware.objects.prefetch_related(
        'manufacturer',
        'device_type',
        'module_type'
    ).annotate(
        instance_count=count_related(models.FirmwareAssignment,'firmware'),
    )
    filterset = filtersets.FirmwareFilterSet
    filterset_form = forms.FirmwareFilterForm
    table = tables.FirmwareTable

@register_model_view(models.Firmware, 'edit')
@register_model_view(models.Firmware, 'add', detail=False)
class FirmwareEditView(generic.ObjectEditView):
    queryset = models.Firmware.objects.all()
    form = forms.FirmwareForm
    default_return_url = 'plugins:netbox_firmware:firmware_list'
    
    def get_initial(self):
        initial = super().get_initial()
        if 'manufacturer' in self.request.GET:
            initial['manufacturer'] = self.request.GET.get('manufacturer')
        if 'device_type' in self.request.GET:
            initial['device_type'] = self.request.GET.get('device_type')
        if 'module_type' in self.request.GET:
            initial['module_type'] = self.request.GET.get('module_type')
        return initial

@register_model_view(models.Firmware,'delete')
class FirmwareDeleteView(generic.ObjectDeleteView):
    queryset = models.Firmware.objects.all()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# ----------------- Bulk Import, Edit, Delete -----------------

@register_model_view(models.Firmware, 'bulk_import', detail=False)
class FirmwareBulkImportView(generic.BulkImportView):
    queryset = models.Firmware.objects.all()
    model_form = forms.FirmwareImportForm

    def save_object(self, object_form, request):
        obj = object_form.save()
        return obj
    
@register_model_view(models.Firmware, 'bulk_edit', detail=False)
class FirmwareBulkEditView(generic.BulkEditView):
    queryset = models.Firmware.objects.all()
    filterset = filtersets.FirmwareFilterSet
    table = tables.FirmwareTable
    form = forms.FirmwareBulkEditForm
    default_return_url = 'plugins:netbox_firmware:firmware_list'
    
    def post (self, request, **kwargs):
        return super().post(request, **kwargs)

@register_model_view(models.Firmware, 'bulk_delete', detail=False)
class FirmwareBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Firmware.objects.all()
    table = tables.FirmwareTable

    def post(self, request):
        return super().post(request)