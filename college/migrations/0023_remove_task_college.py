# Generated by Django 5.0.2 on 2024-02-21 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0022_task_college'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='college',
        ),
    ]
