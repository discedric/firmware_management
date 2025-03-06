# Generated by Django 5.1.6 on 2025-03-06 13:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0200_populate_mac_addresses'),
        ('firmware_management', '0003_firmwareassignment_device_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='firmwareassignment',
            name='firmware',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='FirmwareAssignment', to='firmware_management.firmware'),
        ),
        migrations.AlterField(
            model_name='firmwareassignment',
            name='inventory_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='FirmwareAssignment', to='dcim.inventoryitem'),
        ),
    ]
