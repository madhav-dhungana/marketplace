# Generated by Django 4.0.4 on 2022-05-18 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_alter_user_hourly_rate_alter_user_overview'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='title',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]