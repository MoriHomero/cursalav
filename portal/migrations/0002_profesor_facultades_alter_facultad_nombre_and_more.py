# Generated by Django 5.0.6 on 2024-07-13 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesor',
            name='facultades',
            field=models.ManyToManyField(blank=True, related_name='profesores', to='portal.facultad'),
        ),
        migrations.AlterField(
            model_name='facultad',
            name='nombre',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='materia',
            unique_together={('nombre', 'facultad')},
        ),
    ]
