from django_tables2 import tables

from netbox.tables import NetBoxTable, columns
from ..models import Firmware, FirmwareAssignment

from dcim.tables import DeviceTypeTable, ModuleTypeTable, RackTypeTable
from utilities.tables import register_table_column

__all__ = (
    'FirmwareTable',
    'FirmwareAssignmentTable',
)

class FirmwareTable(NetBoxTable):
    """"
     zorg voor een counter zodat je ziet hoeveel keer deze assigned is
    """
    name = tables.Column(
        linkify=True,
    )
    file_name = tables.Column()
    description = tables.Column()
    comments = tables.Column()
    status = tables.Column()
    manufacturer = tables.Column(
        verbose_name="Manufacturer",
        accessor='manufacturer',
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
    actions = columns.ActionsColumn()

    class Meta(NetBoxTable.Meta):
        model = Firmware
        fields = ('name', 'file_name', 'comments', 'status', 
                  'manufacturer', 
                  'module_type', 'device_type',
                  'actions'
                  )
        

class FirmwareAssignmentTable(NetBoxTable):
    description = tables.Column()
    ticket_number = tables.Column()
    patch_date = tables.Column()
    firmware = tables.Column(accessor='firmware',verbose_name='Firmware',linkify=True,)
    manufacturer = tables.Column(accessor='manufacturer', verbose_name="Manufacturer",linkify=True,)
    device_type = tables.Column(accessor='device_type',verbose_name="Device Type",linkify=True,)
    module_type = tables.Column(accessor='module_type',linkify=True,)
    module = tables.Column(accessor='module',verbose_name="Module",linkify=True,)
    device = tables.Column(accessor='device',verbose_name="Device",linkify=True,)

    class Meta(NetBoxTable.Meta):
        model = FirmwareAssignment
        fields = ('description','ticket_number','patch_date',
                  'firmware','manufacturer',
                  'device_type','device',
                  'module','module_type'
                  )
        default_columns=(
            'firmware', 'description', 'patch_date', 
            'device', 'module',
            'manufacturer', 'ticket_number',
        )
        

