# Generated by Django 4.2.4 on 2023-08-02 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0007_rename_log_hallpass_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hallpass',
            options={'permissions': (('can_view_log_history', 'can_edit_log_history'),), 'verbose_name_plural': 'hall passes'},
        ),
    ]
