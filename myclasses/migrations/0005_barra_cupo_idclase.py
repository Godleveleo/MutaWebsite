# Generated by Django 4.0.3 on 2022-10-31 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myclasses', '0004_barra_cupo'),
    ]

    operations = [
        migrations.AddField(
            model_name='barra_cupo',
            name='idClase',
            field=models.PositiveIntegerField(null=True, verbose_name='de que clase'),
        ),
    ]
