# Generated by Django 5.0.2 on 2024-02-19 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0016_alter_timeline_college'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='college',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='college.college'),
        ),
    ]
