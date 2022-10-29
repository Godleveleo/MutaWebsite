# Generated by Django 3.2.13 on 2022-10-28 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myclasses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('box', models.CharField(max_length=20, null=True, verbose_name='Gimnasio')),
                ('ubicacion', models.CharField(max_length=20, null=True, verbose_name='Ubicación')),
                ('descripcion', models.CharField(max_length=400, null=True, verbose_name='Reseña')),
                ('user_creador', models.CharField(max_length=40, null=True, verbose_name='creado')),
                ('logo', models.ImageField(default='logo/sinfoto.png', upload_to='logo', verbose_name='logo')),
            ],
            options={
                'verbose_name': 'Gimnasio',
                'verbose_name_plural': 'Gimnasios',
            },
        ),
        migrations.CreateModel(
            name='Clases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_creador', models.CharField(max_length=40, null=True, verbose_name='creado')),
                ('Descripcion', models.CharField(max_length=50, null=True)),
                ('modalidad', models.CharField(choices=[('Online', 'Online'), ('Presencial', 'Presencial')], max_length=30, null=True, verbose_name='Modalidad de clase')),
                ('inicioClase', models.CharField(max_length=50, null=True, verbose_name='Inicio de clase')),
                ('TerminoClase', models.CharField(max_length=50, null=True, verbose_name='Termino de clase')),
                ('duracion', models.PositiveIntegerField(default=1, verbose_name='Duracion de Clase')),
                ('cupo', models.PositiveIntegerField(default=1, verbose_name='Nro. de cupos')),
            ],
            options={
                'verbose_name': 'Clases',
                'verbose_name_plural': 'Clases',
            },
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('codigo', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=50, verbose_name='Disciplina')),
                ('horario', models.CharField(choices=[('AM', 'Mañana'), ('PM', 'Tarde'), ('AM/PM', 'AM/PM')], max_length=13, verbose_name='Horario de clases')),
                ('user_creador', models.CharField(max_length=40, null=True, verbose_name='creado')),
            ],
            options={
                'verbose_name': 'Disciplina',
                'verbose_name_plural': 'Disciplinas',
            },
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula', models.CharField(max_length=200, null=True, verbose_name='Alumno Matriculado')),
                ('plan', models.CharField(max_length=200, null=True, verbose_name='Disciplina')),
                ('disInscrita', models.CharField(max_length=200, null=True, verbose_name='Disciplina')),
                ('vigencia', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Alumno matriculado',
                'verbose_name_plural': 'Alumnos matriculados',
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vigencia', models.BooleanField(default=True, verbose_name='Vigente')),
                ('imagenPerfil', models.ImageField(default='perfil/sinfoto.png', upload_to='perfil', verbose_name='Imagen de Perfil')),
                ('DisciplinaInscrita', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myclasses.disciplina', verbose_name='Disciplina inscrita')),
            ],
            options={
                'verbose_name': 'Perfiles',
                'verbose_name_plural': 'Perfiles',
            },
        ),
        migrations.CreateModel(
            name='Planes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30, verbose_name='Nombre del plan')),
                ('disciplina', models.CharField(max_length=40, verbose_name='Displinina')),
                ('horario', models.CharField(choices=[('AM', 'Mañana'), ('PM', 'Tarde'), ('AM/PM', 'AM/PM')], max_length=13, verbose_name='Horario del plan')),
                ('precio', models.PositiveIntegerField(verbose_name='Precio del  plan')),
                ('cantidad_clases', models.PositiveSmallIntegerField(default=1, verbose_name='Clases por Semana')),
                ('user_creador', models.CharField(max_length=40, null=True, verbose_name='creado')),
            ],
            options={
                'verbose_name': 'Planes',
                'verbose_name_plural': 'Planes',
            },
        ),
        migrations.CreateModel(
            name='UsersMetadata',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ced_identidad', models.CharField(max_length=9, verbose_name='Cedula de identidad')),
                ('fechaNacimiento', models.DateField(null=True, verbose_name='Fecha de Nacimiento')),
                ('sexo', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino'), ('N.N', 'Prefiero no Decirlo')], default='Prefiero no Decirlo', max_length=30)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User metadata',
                'verbose_name_plural': 'User metadata',
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clase', models.ForeignKey(max_length=100, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myclasses.clases', verbose_name='Clase reservada')),
                ('gym', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, to='myclasses.box', verbose_name='Gimnasio')),
                ('tipoDisciplina', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myclasses.disciplina', verbose_name='Disciplina')),
                ('usuario', models.ForeignKey(max_length=100, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myclasses.perfil', verbose_name='Alumno')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
            },
        ),
        migrations.AddField(
            model_name='perfil',
            name='nombre',
            field=models.ForeignKey(max_length=100, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myclasses.usersmetadata', verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='perfil',
            name='plan',
            field=models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myclasses.planes', verbose_name='Plan Inscrito'),
        ),
    ]
