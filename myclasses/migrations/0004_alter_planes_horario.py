# Generated by Django 4.0.3 on 2022-10-04 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myclasses', '0003_planes_cantidadclases_alter_disciplina_horario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planes',
            name='horario',
            field=models.CharField(max_length=30),
        ),
    ]
