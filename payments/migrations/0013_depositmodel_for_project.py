# Generated by Django 4.0.4 on 2022-07-17 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_project_payment_added'),
        ('payments', '0012_alter_depositmodel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='depositmodel',
            name='for_project',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
    ]