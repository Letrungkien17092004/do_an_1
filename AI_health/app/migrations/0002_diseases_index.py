# Generated by Django 5.1.2 on 2024-11-17 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diseases',
            name='index',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]