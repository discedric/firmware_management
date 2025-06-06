import django_filters
from django.db.models import Q
from utilities.filters import (
    ContentTypeFilter, MultiValueCharFilter, MultiValueMACAddressFilter, MultiValueNumberFilter, MultiValueWWNFilter,
    NumericArrayFilter, TreeNodeMultipleChoiceFilter,
)
from django.utils.translation import gettext as _
from dcim.models import DeviceType, Manufacturer, ModuleType, Device, Module
from netbox_firmware.choices import FirmwareStatusChoices, HardwareKindChoices

from netbox.filtersets import NetBoxModelFilterSet
from ..models import Firmware, FirmwareAssignment

class FirmwareFilterSet(NetBoxModelFilterSet):
    name = MultiValueCharFilter(
        lookup_expr='iexact',
    )
    file_name = MultiValueCharFilter(
        lookup_expr='icontains',
        label=_('File name'),
    )
    status = django_filters.MultipleChoiceFilter(
        choices=FirmwareStatusChoices,
        label=_('Status'),
    )
    kind = MultiValueCharFilter(
        method='filter_kind',
        label='Type of hardware',
    )
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Manufacturer.objects.all(),
        label=_('Manufacturer (ID)'),
        method='filter_by_manufacturer',  # Custom filter method
    )
    device = django_filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        method='filter_by_device',
        label=_('Device'),
    )
    module = django_filters.ModelChoiceFilter(
        queryset=Module.objects.all(),
        method='filter_by_module',
        label=_('Module'),
    )
    device_type = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type__slug',
        queryset=DeviceType.objects.all(),
        to_field_name='slug',
        label=_('Device type name (slug)'),
    )
    device_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type',
        queryset=DeviceType.objects.all(),
        label=_('Device type (ID)'),
    )
    module_type = django_filters.ModelMultipleChoiceFilter(
        field_name='module_type__model',
        queryset=ModuleType.objects.all(),
        to_field_name='name',
        label=_('Module type (model)'),
    )
    module_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ModuleType.objects.all(),
        label=_('Module type (ID)'),
    )
    
    class Meta:
        model = Firmware
        fields = {
            'id', 'name', 'file_name', 'status',
            'device_type', 'module_type'
        }
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value.strip()) |
            Q(comments__icontains=value)  |
            Q(device_type__slug__icontains=value) |
            Q(module_type__model__icontains=value) |
            Q(device_type__manufacturer__slug__icontains=value) |
            Q(module_type__manufacturer__slug__icontains=value)
        ).distinct()
    
    def filter_kind(self, queryset, name, value):
        query = None
        for kind in HardwareKindChoices.values():
            if kind in value:
                q = Q(**{f'{kind}_type__isnull': False})
                if query:
                    query = query | q
                else:
                    query = q
        if query:
            return queryset.filter(query)
        else:
            return queryset

    def filter_by_device(self, queryset, name, value):
        return queryset.filter(device_type=value.device_type)

    def filter_by_module(self, queryset, name, value):
        return queryset.filter(module_type=value.module_type)

    def filter_by_manufacturer(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(device_type__manufacturer__in=value) |
                Q(module_type__manufacturer__in=value)
            ).distinct()
        return queryset

class FirmwareAssignmentFilterSet(NetBoxModelFilterSet):
    description = MultiValueCharFilter(
        lookup_expr='icontains',
    )
    ticket_number = MultiValueCharFilter(
        lookup_expr='icontains',
        label=_('Ticket number'),
    )
    patch_date = django_filters.DateFromToRangeFilter(
        label=_('Patch date'),
    )
    comment = MultiValueCharFilter(
        lookup_expr='icontains',
    )
    firmware = django_filters.ModelMultipleChoiceFilter(
        field_name='firmware__name',
        queryset=Firmware.objects.all(),
        to_field_name='name',
        label=_('Firmware'),
    )
    firmware_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Firmware.objects.all(),
        label=_('Firmware (ID)'),
    )
    device = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        field_name='device__name',
        to_field_name='name',
        label=_('Device (name)'),
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        label=_('Device (ID)'),
    )
    module_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Module.objects.all(),
        label=_('Module (ID)'),
    )
    kind = MultiValueCharFilter(
        method='filter_kind',
        label='Type of hardware',
    )
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Manufacturer.objects.all(),
        label=_('Manufacturer (ID)'),
        method='filter_by_manufacturer',  # Custom filter method
    )
    module_device = django_filters.ModelMultipleChoiceFilter(
        queryset=Module.objects.all(),
        field_name='module__device',
        label=_('Module (device)'),
    )
    module_device_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        field_name='module__device_id',
        label=_('Module (device ID)'),
    )
    module_sn = django_filters.ModelMultipleChoiceFilter(
        queryset=Module.objects.all(),
        field_name='module__serial',
        label=_('Module (serial)'),
    )
    device_sn = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        field_name='device__serial',
        label=_('Device (serial)'),
    )
    device_type = django_filters.ModelMultipleChoiceFilter(
        queryset=DeviceType.objects.all(),
        field_name='device__device_type__slug',
        to_field_name='slug',
        label=_('Device type (slug)'),
    )
    device_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=DeviceType.objects.all(),
        field_name='device__device_type',
        label=_('Device type (ID)'),
    )
    module_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ModuleType.objects.all(),
        field_name='module__module_type',
        label=_('Module type (ID)'),
    )


    class Meta:
        model = FirmwareAssignment
        fields = {
            'id', 'description', 'ticket_number', 'patch_date', 'comment',
            'firmware', 'device', 'module',
        }
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(description__icontains=value) |
            Q(ticket_number__icontains=value) |
            Q(comment__icontains=value) |
            Q(firmware__name__icontains=value) |
            Q(device__device_type__slug__icontains=value) |
            Q(module__module_type__model__icontains=value) |
            Q(device__name__icontains=value) |
            Q(device__serial__icontains=value) |
            Q(module__serial__icontains=value) |
            Q(manufacturer__slug__icontains=value)
        ).distinct()

    def filter_kind(self, queryset, name, value):
        query = None
        for kind in HardwareKindChoices.values():
            if kind in value:
                q = Q(**{f'{kind}__isnull': False})
                if query:
                    query = query | q
                else:
                    query = q
        if query:
            return queryset.filter(query)
        else:
            return queryset
    
    def filter_by_manufacturer(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(device__device_type__manufacturer__in=value) |
                Q(module__module_type__manufacturer__in=value)
            ).distinct()
        return queryset