# Generated by Django 4.0.3 on 2022-10-11 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myclasses', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matricula',
            old_name='DisInscrita',
            new_name='disInscrita',
        ),
    ]
