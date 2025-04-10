from django.template import Template
from netbox.plugins import PluginTemplateExtension

from .models import Firmware, FirmwareAssignment
from .utils import query_located


WARRANTY_PROGRESSBAR = '''
{% with record.warranty_progress as wp %}
{% with record.warranty_remaining as wr %}
{% with settings.PLUGINS_CONFIG.netbox_inventory.firmware_warranty_expire_warning_days as wthresh %}

{% if wp is None and wr.days <= 0 %}
  <div class="progress" role="progressbar">
    <div class="progress-bar progress-bar-striped text-bg-danger" style="width:100%;">
      Expired {{ record.warranty_end|timesince|split:','|first }} ago
    </div>
  </div>
{% elif wp is None and wr.days > 0 %}
  <div class="progress" role="progressbar">
    <div class="progress-bar progress-bar-striped text-bg-{% if wthresh and wr.days < wthresh %}warning{% else %}success{% endif %}" style="width:100%;">
      {{ record.warranty_end|timeuntil|split:','|first }}
    </div>
  </div>
{% elif wp is None %}
    {{ ""|placeholder }}
{% else %}

<div
  class="progress"
  role="progressbar"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-valuenow="{% if wp < 0 %}0{% else %}{{ wp }}{% endif %}"
>
  <div
    class="progress-bar text-bg-{% if wp >= 100 %}danger{% elif wthresh and wr.days < wthresh %}warning{% else %}success{% endif %}"
    style="width: {% if wp < 0 %}0%{% else %}{{ wp }}%{% endif %};"
  ></div>
  {% if record.warranty_progress >= 100 %}
    <span class="justify-content-center d-flex align-items-center position-absolute text-light w-100 h-100">Expired {{ record.warranty_end|timesince|split:','|first }} ago</span>
  {% elif record.warranty_progress >= 35 %}
    <span class="justify-content-center d-flex align-items-center position-absolute text-body-emphasis w-100 h-100">{{ record.warranty_end|timeuntil|split:','|first }}</span>
  {% elif record.warranty_progress >= 0 %}
    <span class="justify-content-center d-flex align-items-center position-absolute text-body-emphasis w-100 h-100">{{ record.warranty_end|timeuntil|split:','|first }}</span>
  {% else %}
    <span class="justify-content-center d-flex align-items-center position-absolute text-body-emphasis w-100 h-100">Starts in {{ record.warranty_start|timeuntil|split:','|first }}</span>
  {% endif %}
</div>

{% endif %}
{% endwith wthresh %}
{% endwith wr %}
{% endwith wp %}
'''

class FirmwareAssignedInfoExtension(PluginTemplateExtension):
    def right_page(self):
        object = self.context.get('object')
        assignment = FirmwareAssignment.objects.filter(**{f'{self.kind}_id':object.id}).first()
        context = {
          'assignment': assignment
        }
        return self.render('firmware_management/inc/firmware_info.html', extra_context=context)

class DeviceFirmwareInfo(FirmwareAssignedInfoExtension):
    """_summary_
      We willen in het scherm van de device zien welke firmware erop zit.
    """
    models = ['dcim.device']
    kind = 'device'

class ModuleFirmwareInfo(FirmwareAssignedInfoExtension):
    models = ['dcim.module']
    kind = 'module'

class InventoryItemFirmwareInfo(FirmwareAssignedInfoExtension):
    models = ['dcim.inventoryitem']
    kind = 'inventoryitem'

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
                    'extra_filter': '&sort=device_type',
                    'count': count_device,
                },
                {
                    'label': 'Modules',
                    'filter_field': 'manufacturer_id',
                    'extra_filter': '&sort=module_type',
                    'count': count_module,
                },
                {
                    'label': 'Total',
                    'filter_field': 'manufacturer_id',
                    'count': count_device + count_module,
                },
            ],
        }
        return self.render('firmware_management/inc/firmware_stats_counts.html', extra_context=context)

template_extensions = (
    DeviceFirmwareInfo,
    ModuleFirmwareInfo,
    InventoryItemFirmwareInfo,
    ManufacturerFirmwareCounts,
)