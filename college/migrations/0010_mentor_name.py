# Generated by Django 5.0.2 on 2024-02-18 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0009_remove_mentor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]