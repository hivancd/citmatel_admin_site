# Generated by Django 5.0.1 on 2024-12-27 02:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Year',
            fields=[
                ('number', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Año')),
                ('projects', models.ManyToManyField(to='projects.project')),
            ],
        ),
        migrations.AddField(
            model_name='month',
            name='year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='projects.year'),
            preserve_default=False,
        ),
    ]
