from django.db import models
from django.forms import ValidationError
from django.urls import reverse

from ..choices import HardwareKindChoices, FirmwareStatusChoices
from netbox.models import NetBoxModel, ChangeLoggedModel, NestedGroupModel
from netbox_inventory.models import InventoryItemType
from dcim.models import Manufacturer, DeviceType, ModuleType, InventoryItem, Device, Module
from dcim.choices import DeviceStatusChoices

class Bios(NetBoxModel):
    #
    # fields that identify bios
    #
    """_summary_
        toe te voegen:
        - (als kan) hyperlinks
    """
    name = models.CharField(
        help_text='Name of the bios',
        max_length=255,
        verbose_name='Name',
    )
    file_name = models.CharField(
        help_text='File name of the bios',
        blank=True,
        null=True,
        max_length=255,
        verbose_name='File Name',
    )
    file = models.FileField(
        upload_to='bios-files',
        help_text='File of the bios',
        blank=True,
        null=True,
        verbose_name='File',
    )
    status = models.CharField(
        max_length=50,
        choices= DeviceStatusChoices,
        default= DeviceStatusChoices.STATUS_ACTIVE,
        help_text='Firmware lifecycle status',
    )
    description = models.CharField(
        help_text='Description of the bios',
        max_length=255,
        verbose_name='Description',
        null=True,
        blank=True
    )
    comments = models.TextField(
        blank=True,
        null=True,
        help_text='Additional comments about the bios',
    )
    
    #
    # hardware type fields
    #
    device_type = models.ForeignKey(
        to=DeviceType,
        on_delete=models.PROTECT,
        related_name='bios',
        blank=True,
        null=True,
        verbose_name='Device Type',
    )
    inventory_item_type = models.ForeignKey(
        to=InventoryItemType,
        on_delete=models.PROTECT,
        related_name='bios',
        blank=True,
        null=True,
        verbose_name='Inventory Item Type',
    )
    module_type = models.ForeignKey(
        to=ModuleType,
        on_delete=models.PROTECT,
        related_name='bios',
        blank=True,
        null=True,
        verbose_name='Module Type',
    )
    
    clone_fields = [
        'name','description', 'file_name', 'status', 'device_type',
        'inventory_item_type', 'comments', 'module_type'
    ]

    @property
    def kind(self):
        if self.device_type_id:
            return 'device'
        elif self.inventory_item_type_id:
            return 'inventoryitem'
        elif self.module_type_id:
            return 'module'
        else:
            return None
        
    def get_kind_display(self):
        return dict(HardwareKindChoices)[self.kind]
    
    @property
    def hardware_type(self):
        return self.device_type or self.inventory_item_type or self.module_type or None
    
    def clean(self):
        return super().clean()

    def validate_hardware_type(self):
        if(
            sum(
                map(
                    bool,
                    [
                        self.device_type,
                        self.inventory_item_type,
                        self.module_type
                    ],
                )
            )
            > 1
        ):
            raise ValidationError(
                'Only one of device type, inventory item type or module type can be set'
            )
        if (
            not self.device_type
            and not self.inventory_item_type
            and not self.module_type
        ):
            raise ValidationError(
                'One of device type, inventory item type or module type must be set'
        )

    def get_absolute_url(self):
        return reverse('plugins:firmware_management:bios', args=[self.pk])
    
    @classmethod
    def get_fields(cls):
        return {field.name: field for field in cls._meta.get_fields()}
    
    class Meta:
        ordering = ('name','device_type', 'module_type', 'inventory_item_type',)
        unique_together = ('name', 'device_type', 'module_type', 'inventory_item_type')
        verbose_name = 'Bios'
        verbose_name_plural = 'Bios'
        constraints = [
            models.CheckConstraint(
                check=models.Q(device_type__isnull=False) | models.Q(module_type__isnull=False) | models.Q(inventory_item_type__isnull=False),
                name='bios_device_type_or_inventory_item_type_or_module_type_required'
            )
        ]

    def __str__(self):
        return f'{self.name}'


class BiosAssignment(NetBoxModel):
    description = models.TextField(blank=True, null=True)
    ticket_number = models.CharField(max_length=100, blank=True, null=True)
    patch_date = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    bios = models.ForeignKey(
        to=Bios,
        related_name='BiosAssignment',
        on_delete=models.PROTECT,
        verbose_name='Bios',
        null=True,
        blank=True
    )
    module = models.ForeignKey(
        to=Module,
        related_name='BiosAssignment',
        on_delete=models.PROTECT,
        verbose_name='Module',
        null=True,
        blank=True
    )
    device = models.ForeignKey(
        to=Device, 
        related_name='BiosAssignment',
        on_delete=models.PROTECT,
        verbose_name='Device',
        null=True, 
        blank=True
    )
    inventory_item = models.ForeignKey(
        to=InventoryItem, 
        related_name='BiosAssignment',
        on_delete=models.PROTECT,
        verbose_name='Inventory Item',
        null=True, 
        blank=True
    )

    clone_fields = [
        'bios', 'patch_date',
    ]

    class Meta:
        """
        check constraints to ensure that either a device, module or inventory item type is set
        """
        ordering = ('bios', 'device', 'module', 'inventory_item')
        verbose_name = 'Bios Assignment'
        verbose_name_plural = 'Bios Assignments'
        constraints = [
            models.CheckConstraint(
                check=models.Q(device__isnull=False) | models.Q(module__isnull=False) | models.Q(inventory_item__isnull=False),
                name='bios_device_or_module_or_inventory_item_required'
            ),
        ]

    def __str__(self):
        if self.device:
            return f"{self.bios} - {self.device}"
        elif self.module:
            return f"{self.bios} - {self.module}"
        elif self.inventory_item:
            return f"{self.bios} - {self.inventory_item}"
        else:
            return f"{self.bios} - None"