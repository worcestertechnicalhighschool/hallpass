# Generated by Django 4.2.4 on 2023-08-02 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0008_alter_hallpass_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='destinations',
            field=models.ManyToManyField(blank=True, to='passes.destination'),
        ),
    ]
