from django_tables2 import tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, columns
from ..models import Firmware, FirmwareAssignment
from netbox_firmware.utils import FirmwareColumn

from dcim.tables import DeviceTable, ModuleTable
from utilities.tables import register_table_column

__all__ = (
    'FirmwareTable',
    'FirmwareAssignmentTable',
)

class FirmwareTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )
    file_name = tables.Column()
    description = tables.Column()
    comments = tables.Column()
    status = tables.Column()
    manufacturer = tables.Column(
        verbose_name=_('Manufacturer'),
        accessor='manufacturer',  # We gebruiken de method manufacturer
        linkify=True,
    )
    device_type = tables.Column(
        accessor='device_type',
        linkify=True,
        )
    module_type = tables.Column(
        accessor='module_type',
        linkify=True,
        )
    instance_count = columns.LinkedCountColumn(
        viewname='plugins:netbox_firmware:firmwareassignment_list',
        url_params={'firmware_id': 'pk'},
        verbose_name=_('Instances')
    )
    filename = tables.Column(
        accessor='filename',
        verbose_name=_('File path'),
        orderable=False
    )

    class Meta(NetBoxTable.Meta):
        model = Firmware
        fields = ('name', 'file_name', 'comments', 'status', 
                  'manufacturer', 
                  'module_type', 'device_type'
                  )
        #░ Default columns moeten nog gedefinieerd worden in de Meta class

    def order_manufacturer(self, queryset, is_descending):
        if is_descending:
            ordering_device = '-device_type__manufacturer'
            ordering_module = '-module_type__manufacturer'
        else:
            ordering_device = 'device_type__manufacturer'
            ordering_module = 'module_type__manufacturer'
    
        # Voeg de twee velden toe aan de query voor een gecombineerde sortering
        queryset = queryset.order_by(ordering_device, ordering_module)
        return queryset, True  

class FirmwareAssignmentTable(NetBoxTable):
    description = tables.Column()
    ticket_number = tables.Column()
    patch_date = tables.Column()
    firmware = tables.Column(accessor='firmware',verbose_name='Firmware',linkify=True,)
    module = tables.Column(accessor='module',verbose_name="Module",linkify=True,)
    module_device= tables.Column(accessor='module_device',verbose_name='Module owner',linkify=True)
    device = tables.Column(accessor='device',verbose_name="Device",linkify=True,)
    manufacturer = tables.Column(
        verbose_name=_('Manufacturer'),
        accessor='get_manufacturer',  # We gebruiken de method get_manufacturer
        linkify=True,
    )
    
    device_type = tables.Column(accessor='device_type',verbose_name='Device Type',linkify=True)
    device_sn = tables.Column(accessor='device_sn',verbose_name='Device Serial Number')
    module_type = tables.Column(accessor='module_type',verbose_name='Module Type',linkify=True)
    module_sn = tables.Column(accessor='module_sn',verbose_name='Module Serial Number')
    
    class Meta(NetBoxTable.Meta):
        model = FirmwareAssignment
        fields = ('description', 'ticket_number', 'patch_date', 
                  'firmware', 'module_device',
                  'manufacturer', 
                  'device','device_type', 'device_sn',
                  'module','module_type', 'module_sn',
                  )
        default_columns=(
            'firmware', 'description', 'patch_date', 
            'device', 'module',
            'manufacturer', 'ticket_number',
        )
    
    # Order methods required for non database fields
    def order_manufacturer(self, queryset, is_descending):
        if is_descending:
            ordering_device = '-device__device_type__manufacturer'
            ordering_module = '-module__module_type__manufacturer'
        else:
            ordering_device = 'device__device_type__manufacturer'
            ordering_module = 'module__module_type__manufacturer'
    
        # Voeg de twee velden toe aan de query voor een gecombineerde sortering
        queryset = queryset.order_by(ordering_device, ordering_module)
        return queryset, True

    def order_device_sn(self, queryset, is_descending):
        ordering = ('-device__serial' if is_descending else 'device__serial')
        queryset = queryset.order_by(ordering)
        return queryset, True

    def order_module_device(self, queryset, is_descending):
        ordering = ('-module__device' if is_descending else 'module__device')
        queryset = queryset.order_by(ordering)
        return queryset, True
    
    def order_module_sn(self, queryset, is_descending):
        ordering = ('-module__serial' if is_descending else 'module__serial')
        queryset = queryset.order_by(ordering)
        return queryset, True

    def order_device_type(self, queryset, is_descending):
        ordering = ('-device__device_type__model' if is_descending else 'device__device_type__model')
        queryset = queryset.order_by(ordering)
        return queryset, True

    def order_module_type(self, queryset, is_descending):
        ordering = ('-module__module_type__model' if is_descending else 'module__module_type__model')
        queryset = queryset.order_by(ordering)
        return queryset, True

# ========================
# DCIM model table columns
# ========================

firmware_column = FirmwareColumn(
    verbose_name=_('Firmware'),
    orderable=True,
)

register_table_column(firmware_column, 'FirmwareAssignment', DeviceTable)
register_table_column(firmware_column, 'FirmwareAssignment', ModuleTable)
