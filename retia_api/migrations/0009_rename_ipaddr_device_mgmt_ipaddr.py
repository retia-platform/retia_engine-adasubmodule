# Generated by Django 5.0.1 on 2024-01-09 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retia_api', '0008_alter_device_modified_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='ipaddr',
            new_name='mgmt_ipaddr',
        ),
    ]