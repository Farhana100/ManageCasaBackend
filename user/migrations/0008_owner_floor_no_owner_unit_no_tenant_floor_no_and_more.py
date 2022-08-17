# Generated by Django 4.0.6 on 2022-08-15 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_remove_tenant_apartment_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='floor_no',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='owner',
            name='unit_no',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='floor_no',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tenant',
            name='unit_no',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]