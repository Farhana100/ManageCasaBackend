# Generated by Django 4.0.6 on 2022-07-18 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_remove_owner_building_remove_tenant_building'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenant',
            name='apartment_owner',
        ),
    ]
