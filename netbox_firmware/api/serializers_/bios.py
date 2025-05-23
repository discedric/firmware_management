from netbox.api.serializers import NetBoxModelSerializer
from dcim.api.serializers import DeviceTypeSerializer, ManufacturerSerializer, ModuleTypeSerializer
from netbox_firmware.models import Bios, BiosAssignment


class BiosSerializer(NetBoxModelSerializer):
    class Meta:
        model = Bios
        fields = '__all__'


class BiosAssignmentSerializer(NetBoxModelSerializer):
    bios = BiosSerializer(nested=True, required=True)
    class Meta:
        model = BiosAssignment
        fields = '__all__'