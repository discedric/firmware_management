from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.forms.array import SimpleArrayField
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from firmware_management.models import *
from firmware_management.choices import *
from extras.models import ConfigTemplate
from ipam.models import VRF, IPAddress
from netbox.choices import *
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import (
    CSVChoiceField, CSVContentTypeField, CSVModelChoiceField, CSVModelMultipleChoiceField, CSVTypedChoiceField,
    SlugField,
)
from virtualization.models import Cluster, VMInterface, VirtualMachine
from wireless.choices import WirelessRoleChoices
from jsonschema._keywords import required

class BiosImportForm(NetBoxModelImportForm):
    """_summary_
    Zorgen dat we de hardware type en model meegeven in plaats van de 3 dingen appart
    
    """
    device_type = CSVModelChoiceField(
        label=_('Device type'),
        queryset=DeviceType.objects.all(),
        required=False,
        to_field_name='model',
        help_text=_('Device type model')
    )
    module_type = CSVModelChoiceField(
        label=_('Module type'),
        queryset=ModuleType.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Module type')
    )
    
    hardware_kind = CSVTypedChoiceField(
        label=_('Hardware kind'),
        choices=HardwareKindChoices,
        required=True,
        help_text=_('Type of hardware')
    )
    
    status = CSVChoiceField(
        label=_('Status'),
        choices=DeviceStatusChoices,
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
        fields = ['name', 'file_name', 'status', 'description', 'comments', 'device_type', 'module_type']
        labels = {
            'name': 'Name',
            'file_name': 'File name',
            'status': 'Status',
            'description': 'Description',
            'comments': 'Comments',
            'device_type': 'Device type',
            'module_type': 'Module type',
        }
        help_texts = {
            'name': 'Name of the firmware',
            'file_name': 'File name of the firmware',
            'status': 'Firmware lifecycle status',
            'description': 'Description of the firmware',
            'comments': 'Additional comments about the firmware',
            'device_type': 'The type of device',
            'module_type': 'The type of module',
        }

    def clean(self):
        super().clean()
        # Perform additional validation on the form
        pass

class BiosAssignmentImportForm(NetBoxModelImportForm):
    bios = CSVModelChoiceField(
        label=_('Bios'),
        queryset=Bios.objects.all(),
        to_field_name='name',
        help_text=_('Bios name')
    )
    device = CSVModelChoiceField(
        label=_('Device'),
        queryset=Device.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Device name')
    )
    module = CSVModelChoiceField(
        label=_('Module'),
        queryset=Module.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Module name')
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
        fields = ['bios', 'device', 'module', 'comments', 'patch_date', 'ticket_number', 'description']
        labels = {
            'bios': 'Bios',
            'device': 'Device',
            'module': 'Module',
            'comments': 'Comments',
            'patch_date': 'Patch date',
            'ticket_number': 'Ticket number',
            'description': 'Description',
        }
        help_texts = {
            'bios': 'Bios name',
            'device': 'Device name',
            'module': 'Module name',
            'comments': 'Additional comments about the bios assignment',
            'patch_date': 'Date of the bios patch',
            'ticket_number': 'Ticket number of the bios patch',
            'description': 'Description of the bios assignment',
        }

    def clean(self):
        super().clean()
        # Perform additional validation on the form
        pass