from django.template import Template
from netbox.plugins import PluginTemplateExtension

from .models import Firmware, FirmwareAssignment
from .utils import query_located


class FirmwareAssignedInfoExtension(PluginTemplateExtension):
    def right_page(self):
        object = self.context.get('object')
        assignments = FirmwareAssignment.objects.filter(**{f'{self.kind}_id':object.id}).order_by('-patch_date')[:5]
        context = {
          'assignments': assignments
        }
        return self.render('netbox_firmware/inc/firmware_info.html', extra_context=context)

class DeviceFirmwareInfo(FirmwareAssignedInfoExtension):
    """_summary_
      We willen in het scherm van de device zien welke firmware erop zit.
    """
    models = ['dcim.device']
    kind = 'device'

class ModuleFirmwareInfo(FirmwareAssignedInfoExtension):
    models = ['dcim.module']
    kind = 'module'

class ManufacturerFirmwareCounts(PluginTemplateExtension):
    models = ['dcim.manufacturer']
    def right_page(self):
        object = self.context.get('object')
        user = self.context['request'].user
        count_device = Firmware.objects.restrict(user, 'view').filter(device_type__manufacturer=object).count()
        count_module = Firmware.objects.restrict(user, 'view').filter(module_type__manufacturer=object).count()
        context = {
            'firmware_stats': [
                {
                    'label': 'Devices',
                    'filter_field': 'manufacturer_id',
                    'extra_filter': '&kind=device',
                    'count': count_device,
                },
                {
                    'label': 'Modules',
                    'filter_field': 'manufacturer_id',
                    'extra_filter': '&kind=module',
                    'count': count_module,
                },
                {
                    'label': 'Total',
                    'filter_field': 'manufacturer_id',
                    'count': count_device + count_module,
                },
            ],
        }
        return self.render('netbox_firmware/inc/firmware_stats_counts.html', extra_context=context)


class FirmwareAssignmentsTable(PluginTemplateExtension):
    models = ['netbox_firmware.firmware']
    kind = 'firmware'
  
    def right_page(self):
        object = self.context.get('object')
        assignments = FirmwareAssignment.objects.filter(**{f'{self.kind}':object.id})
        context = {
          #'assignments': assignments.order_by('-id')[:5],
          'count': assignments.count()
        }
        return self.render('netbox_firmware/inc/firmware_assignment_table.html', extra_context=context)


template_extensions = (
    DeviceFirmwareInfo,
    ModuleFirmwareInfo,
    ManufacturerFirmwareCounts,
    FirmwareAssignmentsTable,
)