# Generated by Django 5.0.2 on 2024-02-19 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0011_alter_mentor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(default=1, max_length=100),
        ),
    ]
