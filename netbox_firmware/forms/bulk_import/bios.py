from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from netbox_firmware.models import *
from netbox_firmware.choices import *
from netbox.choices import *
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import (
    CSVChoiceField, CSVContentTypeField, CSVModelChoiceField, CSVModelMultipleChoiceField, CSVTypedChoiceField,
    SlugField,
)

class BiosImportForm(NetBoxModelImportForm):
    hardware_kind = CSVTypedChoiceField(
        label=_('Hardware kind'),
        choices=HardwareKindChoices,
        required=True,
        help_text=_('Type of hardware')
    )
    hardware_type_name = forms.CharField(
        label=_('Hardware Type name'),
        required=True,
        help_text=_('Name of the hardware Type')
    )
    manufacturer= CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Manufacturer name')
    )
    status = CSVChoiceField(
        label=_('Status'),
        choices=BiosStatusChoices,
        help_text=_('Operational status')
    )
    name = forms.CharField(
        label=_('Name'),
        help_text=_('Name of the firmware')
    )
    file_name = forms.CharField(
        label=_('File name'),
        required=False,
        help_text=_('File name of the firmware')
    )
    description = forms.CharField(
        label=_('Description'),
        required=False,
        help_text=_('Description of the firmware')
    )
    comments = forms.CharField(
        label=_('Comments'),
        required=False,
        help_text=_('Additional comments about the firmware')
    )

    class Meta:
        model = Bios
        fields = [
            'name', 
            'file_name', 
            'status', 
            'description', 
            'comments',
            'manufacturer', 
            'hardware_kind', 
            'hardware_type_name', 
            ]

    def clean(self):
        super().clean()
        # Perform additional validation on the form
        pass
    
    def _clean_fields(self):
        return super()._clean_fields()

    def _get_validation_exclusions(self):
        exclude = super()._get_validation_exclusions()
        exclude.remove('device_type')
        exclude.remove('module_type')
        return exclude

    def clean_hardware_type_name(self):
        hardware_kind = self.cleaned_data.get('hardware_kind')
        manufacturer = self.cleaned_data.get('manufacturer')
        model = self.cleaned_data.get('hardware_type_name')
        if not hardware_kind or not manufacturer:
            # clean on manufacturer or hardware_kind already raises
            return None
        if hardware_kind == 'device':
            hardware_class = DeviceType
        elif hardware_kind == 'module':
            hardware_class = ModuleType
        try:
            hardware_type = hardware_class.objects.get(
                manufacturer=manufacturer, model=model
            )
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                f'Hardware type not found: "{hardware_kind}", "{manufacturer}", "{model}"'
            )
        setattr(self.instance, f'{hardware_kind}_type', hardware_type)
        return hardware_type

    def _get_clean_value(self, field_name):
        try:
            return self.base_fields[field_name].clean(self.data.get(field_name))
        except forms.ValidationError as e:
            self.add_error(field_name, e)
            raise

class BiosAssignmentImportForm(NetBoxModelImportForm):
    bios = CSVModelChoiceField(
        label=_('Bios'),
        queryset=Bios.objects.all(),
        to_field_name='name',
        help_text=_('Bios name')
    )
    manufacturer= CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Manufacturer name')
    )
    hardware_kind = CSVTypedChoiceField(
        label=_('Hardware kind'),
        choices=HardwareKindChoices,
        required=True,
        help_text=_('Type of hardware')
    )
    hardware_name = forms.CharField(
        label=_('Hardware name'),
        required=True,
        help_text=_('Name of the hardware, e.g. device name or module id/serial')
    )
    comments = forms.CharField(
        label=_('Comments'),
        required=False,
        help_text=_('Additional comments about the bios assignment')
    )
    patch_date = forms.DateField(
        label=_('Patch date'),
        required=False,
        help_text=_('Date of the bios patch')
    )
    ticket_number = forms.CharField(
        label=_('Ticket number'),
        required=False,
        help_text=_('Ticket number of the bios patch')
    )
    description = forms.CharField(
        label=_('Description'),
        required=False,
        help_text=_('Description of the bios assignment')
    )

    class Meta:
        model = BiosAssignment
        fields = [
            'bios', 
            'manufacturer', 
            'hardware_kind', 
            'hardware_name', 
            'comments', 
            'patch_date', 
            'ticket_number', 
            'description'
            ]

    def clean(self):
        super().clean()
        pass
    
    def _clean_fields(self):
        return super()._clean_fields()

    def _get_validation_exclusions(self):
        exclude = super()._get_validation_exclusions()
        exclude.remove('device')
        exclude.remove('module')
        return exclude

    def clean_hardware_name(self):
        hardware_kind = self.cleaned_data.get('hardware_kind')
        manufacturer = self.cleaned_data.get('manufacturer')
        model = self.cleaned_data.get('hardware_name')
        if not hardware_kind or not manufacturer:
            # clean on manufacturer or hardware_kind already raises
            return None
        
        try:
            if hardware_kind == 'device':
                hardware_type = Device.objects.get(
                    device_type__manufacturer=manufacturer, name=model
                )
                if BiosAssignment.objects.filter(device__name=model).exists():
                    raise ValidationError(f'Device "{model}" already has a BIOS assigned.')
            elif hardware_kind == 'module':
                if model.isdigit():
                    hardware_type = Module.objects.get(
                        module_type__manufacturer=manufacturer, pk=model
                    )
                    if BiosAssignment.objects.filter(module=model).exists():
                        raise ValidationError(f'Module "{model}" already has a BIOS assigned.')
                else:
                    hardware_type = Module.objects.get(
                        module_type__manufacturer=manufacturer, serial=model
                    )
                    if BiosAssignment.objects.filter(module__serial=model).exists():
                         raise ValidationError(f'Module "{model}" already has a BIOS assigned.')
                    
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                f'Hardware type not found: "{hardware_kind}", "{manufacturer}", "{model}"'
            )
        setattr(self.instance, f'{hardware_kind}', hardware_type)
        return hardware_type

    def _get_clean_value(self, field_name):
        try:
            return self.base_fields[field_name].clean(self.data.get(field_name))
        except forms.ValidationError as e:
            self.add_error(field_name, e)
            raise