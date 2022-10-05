# Generated by Django 4.0.3 on 2022-10-04 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myclasses', '0005_estudiante_vigencia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudiante',
            name='cantidad_clases',
        ),
        migrations.AlterField(
            model_name='disciplina',
            name='horario',
            field=models.CharField(choices=[('AM', 'Mañana'), ('PM', 'Tarde'), ('AM/PM', 'AM/PM')], max_length=13, verbose_name='Horario de clases'),
        ),
        migrations.AlterField(
            model_name='disciplina',
            name='tipo',
            field=models.CharField(max_length=50, verbose_name='Disciplina'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='apellidoMaterno',
            field=models.CharField(max_length=35, verbose_name='Apellido Materno'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='apellidoPaterno',
            field=models.CharField(max_length=35, verbose_name='Apellido Paterno'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='ced_identidad',
            field=models.CharField(max_length=9, primary_key=True, serialize=False, verbose_name='Cedula de identidad'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='correo',
            field=models.EmailField(max_length=254, verbose_name='Correo electronico'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='fechaNacimiento',
            field=models.DateField(verbose_name='Fecha de Nacimiento'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='imagenPerfil',
            field=models.ImageField(null=True, upload_to='Foto_Perfil', verbose_name='Imagen de Perfil'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='nombres',
            field=models.CharField(max_length=35, verbose_name='Nombres'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='plan',
            field=models.ForeignKey(max_length=20, on_delete=django.db.models.deletion.DO_NOTHING, to='myclasses.planes', verbose_name='Plan Inscrito'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myclasses.disciplina', verbose_name='Disciplina inscrita'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='vigencia',
            field=models.BooleanField(default=True, verbose_name='Estado del alumno'),
        ),
        migrations.AlterField(
            model_name='planes',
            name='cantidadClases',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Clases por Semana'),
        ),
        migrations.AlterField(
            model_name='planes',
            name='horario',
            field=models.CharField(max_length=30, verbose_name='Inicio de clases'),
        ),
        migrations.AlterField(
            model_name='planes',
            name='precio',
            field=models.CharField(max_length=8, verbose_name='Precio del  plan'),
        ),
    ]