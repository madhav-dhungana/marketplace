# Generated by Django 4.0.4 on 2022-06-25 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_invitemodel_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]