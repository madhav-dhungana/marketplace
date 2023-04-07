# Generated by Django 4.0.4 on 2022-09-26 10:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_subscriber_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='token',
            field=models.UUIDField(default=uuid.UUID('6fdee204-f453-45e6-8f5b-28e7e441d7d2'), editable=False),
        ),
    ]