
# Generated by Django 4.0.6 on 2022-08-28 06:46

# Generated by Django 4.0.6 on 2022-08-28 12:14


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceProvider', '0003_usersubscription_delete_apartmentsubscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='subscription_date',

            field=models.DateTimeField(auto_now_add=True),

            field=models.DateTimeField(auto_now_add=True, null=True),

        ),
    ]
