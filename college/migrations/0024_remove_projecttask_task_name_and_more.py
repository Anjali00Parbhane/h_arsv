# Generated by Django 5.0.2 on 2024-02-25 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0023_remove_task_college'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projecttask',
            name='task_name',
        ),
        migrations.AlterField(
            model_name='projecttask',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('InProgress', 'In Progress'), ('Submitted', 'Submitted'), ('Reassigned', 'Re Assigned')], default='Pending', max_length=20),
        ),
    ]