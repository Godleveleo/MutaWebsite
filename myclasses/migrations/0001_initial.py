# Generated by Django 4.0.3 on 2022-10-04 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('codigo', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=50)),
                ('horario', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('ced_identidad', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('apellidoPaterno', models.CharField(max_length=35)),
                ('apellidoMaterno', models.CharField(max_length=35)),
                ('nombres', models.CharField(max_length=35)),
                ('fechaNacimiento', models.DateField()),
                ('sexo', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino'), ('N.N', 'Prefiero no Decirlo')], default='Prefiero no Decirlo', max_length=30)),
                ('plan', models.CharField(max_length=10)),
                ('cantidad_clases', models.PositiveSmallIntegerField(default=1)),
                ('correo', models.EmailField(max_length=254)),
                ('imagenPerfil', models.ImageField(null=True, upload_to='Foto_Perfil')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myclasses.disciplina')),
            ],
        ),
        migrations.CreateModel(
            name='Incripciones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fechaIncripcion', models.DateTimeField(auto_now_add=True)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myclasses.estudiante')),
            ],
        ),
    ]