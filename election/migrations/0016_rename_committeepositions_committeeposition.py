# Generated by Django 4.0.6 on 2022-08-24 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_remove_owner_floor_no_remove_owner_unit_no_and_more'),
        ('election', '0015_committeepositions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CommitteePositions',
            new_name='CommitteePosition',
        ),
    ]
