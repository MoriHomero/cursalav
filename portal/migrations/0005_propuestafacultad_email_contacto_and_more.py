# Generated by Django 5.0 on 2024-08-07 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_propuestafacultad'),
    ]

    operations = [
        migrations.AddField(
            model_name='propuestafacultad',
            name='email_contacto',
            field=models.EmailField(default=2022, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='propuestafacultad',
            name='mensaje',
            field=models.TextField(blank=True),
        ),
    ]
