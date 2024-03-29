# Generated by Django 4.0.6 on 2022-08-18 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_remove_owner_floor_no_remove_owner_unit_no_and_more'),
        ('election', '0013_committeeelection_no_of_candidates'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitteeMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=30)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now_add=True)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.building')),
                ('committee_election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.committeeelection')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.owner')),
            ],
            options={
                'db_table': 'committee_member',
            },
        ),
    ]
