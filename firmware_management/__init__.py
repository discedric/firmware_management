from netbox.plugins import PluginConfig
from django.urls import include, path
from .version import __version__

class FirmwareManagerConfig(PluginConfig):
    name = 'firmware_management'
    verbose_name = 'Firmware Management'
    version = __version__
    description = 'Firmware management in NetBox'
    author = 'Cedric Vaneessen'
    author_email = 'cedric.vaneessen@zabun.be'
    min_version = '4.1.0'
    default_settings = {
        'top_level_menu': True,
        'used_status_name': 'used',
        'used_additional_status_names': list(),
        'asset_warranty_expire_warning_days': 90,
    }

    def ready(self):
        self.urlpatterns = [
            path('plugins/firmware_management', include('firmware_management.urls'))
        ]
        super().ready()

config = FirmwareManagerConfig