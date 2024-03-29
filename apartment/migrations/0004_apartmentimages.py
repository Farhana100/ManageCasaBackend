# Generated by Django 4.0.6 on 2022-08-17 12:50

import apartment.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0003_alter_apartment_owner_alter_apartment_tenant'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=apartment.models.get_apartment_image_upload_path)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartment.apartment')),
            ],
            options={
                'db_table': 'apartment_image',
            },
        ),
    ]
