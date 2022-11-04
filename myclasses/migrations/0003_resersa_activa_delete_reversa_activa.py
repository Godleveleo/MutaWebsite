# Generated by Django 4.0.3 on 2022-11-04 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myclasses', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resersa_activa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.PositiveIntegerField(null=True, verbose_name='Id del usuario que reserva')),
                ('reserva_id', models.PositiveIntegerField(verbose_name='Id del usuario que reserva')),
                ('comunidad', models.PositiveIntegerField(verbose_name='Id del usuario que reserva')),
                ('fecha', models.DateTimeField(auto_now=True, verbose_name='Id del usuario que reserva')),
            ],
        ),
        migrations.DeleteModel(
            name='Reversa_activa',
        ),
    ]
