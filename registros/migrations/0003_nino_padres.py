# Generated by Django 5.1.6 on 2025-03-08 19:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0002_nino'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='nino',
            name='padres',
            field=models.ManyToManyField(related_name='hijos', to=settings.AUTH_USER_MODEL),
        ),
    ]
