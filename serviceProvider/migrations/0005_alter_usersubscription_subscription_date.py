# Generated by Django 4.0.6 on 2022-08-29 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceProvider', '0004_alter_usersubscription_subscription_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='subscription_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]