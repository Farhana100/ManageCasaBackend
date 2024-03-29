# Generated by Django 4.0.6 on 2022-08-25 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0009_remove_owner_floor_no_remove_owner_unit_no_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_name', models.TextField()),
                ('vote_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'option',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phase', models.CharField(blank=True, max_length=30, null=True)),
                ('selected_option', models.TextField()),
                ('topic', models.TextField()),
                ('description', models.TextField()),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('vote_count', models.IntegerField(default=0)),
                ('no_of_options', models.IntegerField(default=0)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.building')),
            ],
            options={
                'db_table': 'poll',
            },
        ),
        migrations.CreateModel(
            name='PollVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='poll.option')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.owner')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.poll')),
            ],
            options={
                'db_table': 'poll_vote',
            },
        ),
        migrations.AddField(
            model_name='option',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.poll'),
        ),
    ]
