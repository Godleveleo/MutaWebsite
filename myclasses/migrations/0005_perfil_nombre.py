# Generated by Django 4.0.3 on 2022-10-10 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myclasses', '0004_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='nombre',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
