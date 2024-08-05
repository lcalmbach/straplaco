# Generated by Django 5.0.7 on 2024-08-05 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objective_manager_app', '0028_strategiedokument_settings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='strategiedokument',
            name='settings',
        ),
        migrations.AddField(
            model_name='strategie',
            name='settings',
            field=models.JSONField(blank=True, default=dict, null=True, verbose_name='Einstellungen'),
        ),
    ]
