# Generated by Django 4.0.4 on 2022-06-12 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_remove_project_project_period_alter_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('PEN', 'Pending'), ('Active', 'Active'), ('ON', 'Ongoing'), ('COM', 'Completed'), ('CAN', 'Cancelled')], default='PEN', max_length=250),
        ),
    ]