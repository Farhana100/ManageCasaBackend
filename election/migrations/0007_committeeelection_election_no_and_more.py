# Generated by Django 4.0.6 on 2022-08-15 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0006_alter_committeeelection_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='committeeelection',
            name='election_no',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='committeeelection',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
