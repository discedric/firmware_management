# Generated by Django 5.1.6 on 2025-03-04 12:51

import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('extras', '0122_charfield_null_choices'),
        ('netbox_inventory', '0009_add_rack'),
    ]

    operations = [
        migrations.CreateModel(
            name='Firmware',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('file_name', models.CharField(max_length=255)),
                ('status', models.CharField(default='active', max_length=50)),
                ('comment', models.TextField(blank=True, null=True)),
                ('inventory_item_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='netbox_inventory.inventoryitemtype')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FirmwareAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('inventory_item', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('ticket_number', models.CharField(blank=True, max_length=100, null=True)),
                ('patch_date', models.DateField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('inventory_item_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='netbox_inventory.inventoryitemtype')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
