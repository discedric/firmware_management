from django import forms

from dcim.models import DeviceType, Manufacturer, ModuleType, InventoryItem, Device, Module
from netbox_inventory.models import InventoryItemType
from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
)
from utilities.forms.rendering import FieldSet, TabbedGroups

from firmware_management.choices import FirmwareStatusChoices
from firmware_management.models import (
    Bios,
    BiosAssignment
)
from firmware_management.utils import get_plugin_setting

class BiosBulkEditForm(NetBoxModelBulkEditForm):
    name = forms.CharField(required=False, label='Name')
    status = forms.ChoiceField(
        choices=FirmwareStatusChoices,
        required=False,
        label='Status',
    )
    file = forms.FileField(
        required=False,
        label='File',
    )
    description = forms.CharField(
        required=False,
    )
    file_name = forms.CharField(required=False, label='File Name')
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        selector=True,
        label='Manufacturer'
    )
    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        selector=True,
        label='Supported Device Type',
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    module_type = DynamicModelChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        selector=True,
        label='Module Type',
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    inventory_item_type = DynamicModelChoiceField(
        queryset=InventoryItemType.objects.all(),
        required=False,
        selector=True,
        query_params={
           'manufacturer_id': '$manufacturer',
        },
        label='Inventory Item Type',
    )
    comments = CommentField()
    
    model = Bios
    fieldsets=(
        FieldSet('name', 'file_name', 'file', 'status', 'description',name='General'),
        FieldSet(
            'manufacturer',
            TabbedGroups(
                FieldSet('device_type',name='Device Type'),
                FieldSet('module_type',name='Module Type'),
                FieldSet('inventory_item_type',name='Inventory Item Type'),
            ),
            name='Hardware'
        ),
    )
    nullable_fields = ['device_type', 'module_type', 'inventory_item_type']
    

class BiosAssignmentBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        required=False,
    )
    
    # Hardware Items ------------------------
    
    device = DynamicModelChoiceField(
        queryset = Device.objects.all(),
        required=False,
        selector=True,
        label='Device',
    )
    module = DynamicModelChoiceField(
        queryset = Module.objects.all(),
        required=False,
        selector=True,
        label='Module',
    )
    inventory_item = DynamicModelChoiceField(
        queryset = InventoryItem.objects.all(),
        required=False,
        selector=True,
        label='Inventory Item',
    )
    
    # Update --------------------------------
    bios = DynamicModelChoiceField(
        queryset=Bios.objects.all(),
        selector=True,
        required=False,
        label='Bios',
    )
    comment = CommentField()
    patch_date = forms.DateField(
        required=False,
        label='Patch Date',
        help_text='Date of the bios patch'
    )
    ticket_number = forms.CharField(
        required=False,
        label='Ticket Number',
        help_text='Ticket number for the bios patch'
    )
    
    model= BiosAssignment
    fieldsets = (
        FieldSet(
            'description',
            TabbedGroups(
                FieldSet('device',name='Device'),
                FieldSet('module',name='Module'),
                FieldSet('inventory_item',name='Inventory Item'),
            ),
            name='Hardware'
        ),
        FieldSet(
            'ticket_number','bios','patch_date','comment',
            name='Update'
        ),
    )
    nullable_fields = ['device', 'module', 'inventory_item', 'ticket_number', 'patch_date', 'comment']