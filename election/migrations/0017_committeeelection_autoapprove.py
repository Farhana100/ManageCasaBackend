# Generated by Django 4.0.6 on 2022-08-24 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0016_rename_committeepositions_committeeposition'),
    ]

    operations = [
        migrations.AddField(
            model_name='committeeelection',
            name='autoapprove',
            field=models.BooleanField(default=False),
        ),
    ]
