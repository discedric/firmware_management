from dcim.models import DeviceType, Manufacturer, ModuleType, Device, Module
from django import forms
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms.widgets import DatePicker, ClearableFileInput
from firmware_management.utils import get_tags_and_edit_protected_firmware_fields
from firmware_management.filtersets import FirmwareFilterSet, FirmwareAssignmentFilterSet
from firmware_management.models import Firmware, FirmwareAssignment

__all__ = (
    'FirmwareForm',
    'FirmwareAssignmentForm',
)

class FirmwareForm(NetBoxModelForm):
    name = forms.CharField()
    description = forms.CharField(
        required=False,
    )
    file_name = forms.CharField(required=False, label='File Name')
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label='Manufacturer',
        selector=True,
        quick_add=True,
        initial_params={
            'device_types': '$device_type',
        },
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
    comments = CommentField()
    
    fieldsets=(
        FieldSet('name', 'file_name', 'file', 'status', 'description',name='General'),
        FieldSet(
            'manufacturer',
            TabbedGroups(
                FieldSet('device_type',name='Device Type'),
                FieldSet('module_type',name='Module Type'),
            ),
            name='Hardware'
        ),
    )

    class Meta:
        model = Firmware
        fields = [
            'name',
            'file_name',
            'file',
            'description',
            'manufacturer',
            'device_type',
            'module_type',
            'status',
            'comments',
        ]
        widgets = {
            'file': ClearableFileInput(attrs={
                'accept': '.bin,.img,.tar,.tar.gz,.zip,.exe'
                }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_fields_by_tags()
        # Used for picking the default active tab for hardware type selection
        self.no_hardware_type = True
        if self.instance:
            if (
                self.instance.device_type
                or self.instance.module_type
            ):
                self.no_hardware_type = False
    
    def _disable_fields_by_tags(self):
        """
        We need to disable fields that are not editable based on the tags that are assigned to the firmware.
        """
        if not self.instance.pk:
            # If we are creating a new firmware we can't disable fields
            return

        # Disable fields that should not be edited
        tags = self.instance.tags.all().values_list('slug', flat=True)
        tags_and_disabled_fields = get_tags_and_edit_protected_firmware_fields()

        for tag in tags:
            if tag not in tags_and_disabled_fields:
                continue

            for field in tags_and_disabled_fields[tag]:
                if field in self.fields:
                    self.fields[field].disabled = True
    
    
class FirmwareAssignmentForm(NetBoxModelForm):
    """
    Require type before item

    clone add to assigment


    """
    # Hardware ------------------------------
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        selector=True,
        required=True,
        label='Manufacturer',
    )
    description = forms.CharField(
        required=False,
    )
    
    # Hardware Type -------------------------
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
        label='Supported Netbox Inventory Item Type',
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    
    # Hardware Items ------------------------
    
    device = DynamicModelChoiceField(
        queryset = Device.objects.all(),
        required=False,
        selector=True,
        label='Device',
        query_params={
            'manufacturer_id': '$manufacturer',
            'device_type_id': '$device_type',
        },
    )
    module = DynamicModelChoiceField(
        queryset = Module.objects.all(),
        required=False,
        selector=True,
        label='Module',
        query_params={
            'manufacturer_id': '$manufacturer',
            'module_type_id': '$module_type',
        },
    )
    
    # Update --------------------------------
    firmware = DynamicModelChoiceField(
        queryset=Firmware.objects.all(),
        selector=True,
        required=True,
        label='Firmware',
        query_params={
            'status': 'active',
            'manufacturer_id': '$manufacturer',
            'device_type_id': '$device_type',
            'module_type_id': '$module_type',
        },
    )
    comment = CommentField()
    
    fieldsets = (
        FieldSet(
            'manufacturer','description',
            TabbedGroups(
                FieldSet('device_type',name='Device Type'),
                FieldSet('module_type',name='Module Type'),
            ),
            TabbedGroups(
                FieldSet('device',name='Device'),
                FieldSet('module',name='Module'),
            ),
            name='Hardware'
        ),
        FieldSet(
            'ticket_number','firmware','patch_date','comment',
            name='Update'
        ),
    )
    
    class Meta:
        model = FirmwareAssignment
        fields = [
            'description',
            'ticket_number',
            'patch_date',
            'comment',
            'firmware',
            'manufacturer',
            'device_type',
            'device',
            'module_type',
            'module',
        ]
        widgets = {
            'patch_date': DatePicker(),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data