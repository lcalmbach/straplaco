# Generated by Django 5.0.7 on 2024-08-23 14:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objective_manager_app', '0002_wertung_remove_planrecord_monat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='planrecord',
            name='Massnahme',
            field=models.ForeignKey(default=328, on_delete=django.db.models.deletion.CASCADE, to='objective_manager_app.massnahme'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='planrecord',
            name='einhaltung_termin',
            field=models.BooleanField(default=False, null=True, verbose_name='Termin wird eingehalten'),
        ),
        migrations.AlterField(
            model_name='planrecord',
            name='fortschritt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planrecord_fortschritt', to='objective_manager_app.wertung', verbose_name='Zielerreichungsgrad'),
        ),
    ]
