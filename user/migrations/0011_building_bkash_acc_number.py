# Generated by Django 4.0.6 on 2022-08-28 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_building_total_fund_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='bkash_acc_number',
            field=models.IntegerField(default=0),
        ),
    ]