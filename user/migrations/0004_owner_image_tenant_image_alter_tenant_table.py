# Generated by Django 4.0.6 on 2022-07-18 06:40

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_owner_alter_building_table_tenant'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.get_owner_image_upload_path),
        ),
        migrations.AddField(
            model_name='tenant',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.get_tenant_image_upload_path),
        ),
        migrations.AlterModelTable(
            name='tenant',
            table='tenant',
        ),
    ]
