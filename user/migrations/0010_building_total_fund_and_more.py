# Generated by Django 4.0.6 on 2022-08-27 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_remove_owner_floor_no_remove_owner_unit_no_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='total_fund',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='building',
            name='service_charge_amount',
            field=models.FloatField(default=0),
        ),
    ]