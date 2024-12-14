# Generated by Django 5.1.2 on 2024-12-14 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqlService', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicines',
            name='vector',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='prescription_medicines',
            name='medicineId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescription_medicines', to='sqlService.medicines'),
        ),
        migrations.AlterField(
            model_name='prescription_medicines',
            name='prescriptionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescription_medicines', to='sqlService.prescriptions'),
        ),
    ]
