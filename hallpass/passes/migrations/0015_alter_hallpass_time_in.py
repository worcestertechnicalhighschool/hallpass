# Generated by Django 4.2.5 on 2023-09-12 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0014_hallpass_arrival_time_hallpass_cancel_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hallpass',
            name='Time_in',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]