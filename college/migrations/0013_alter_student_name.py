# Generated by Django 5.0.2 on 2024-02-19 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0012_alter_student_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
