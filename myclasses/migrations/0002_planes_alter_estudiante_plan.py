# Generated by Django 4.0.3 on 2022-10-04 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myclasses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Planes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo', models.CharField(max_length=30)),
                ('horario', models.DateTimeField()),
                ('precio', models.CharField(max_length=8)),
            ],
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='plan',
            field=models.ForeignKey(max_length=20, on_delete=django.db.models.deletion.DO_NOTHING, to='myclasses.planes'),
        ),
    ]
