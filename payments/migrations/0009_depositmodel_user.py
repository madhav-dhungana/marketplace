# Generated by Django 4.0.4 on 2022-07-17 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0008_alter_depositmodel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='depositmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_deposits', to=settings.AUTH_USER_MODEL),
        ),
    ]
