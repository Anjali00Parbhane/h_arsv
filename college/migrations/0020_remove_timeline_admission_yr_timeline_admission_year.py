# Generated by Django 5.0.2 on 2024-02-20 10:11

import college.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0019_alter_student_current_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeline',
            name='admission_yr',
        ),
        migrations.AddField(
            model_name='timeline',
            name='admission_year',
            field=models.IntegerField(choices=college.models.year_choices, default=college.models.current_year),
        ),
    ]
