# Generated by Django 4.0.6 on 2022-08-14 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0003_rename_elected_committee_member_committeeelection_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='committeeelection',
            old_name='owner',
            new_name='elected_member',
        ),
    ]
