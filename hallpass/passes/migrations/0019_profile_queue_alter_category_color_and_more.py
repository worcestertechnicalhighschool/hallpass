# Generated by Django 4.2.7 on 2023-11-29 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0018_rename_arrival_time_hallpass_arrival_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='queue',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='color',
            field=models.CharField(default='#eeeeee', max_length=7),
        ),
        migrations.AlterField(
            model_name='category',
            name='text_color',
            field=models.CharField(default='#000000', max_length=7),
        ),
    ]
