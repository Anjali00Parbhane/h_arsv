# Generated by Django 5.0.2 on 2024-02-19 12:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0014_alter_student_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeline',
            name='college',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='college.college'),
        ),
    ]