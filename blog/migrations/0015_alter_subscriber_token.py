# Generated by Django 4.0.4 on 2022-09-26 10:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_blog_slug_alter_subscriber_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='token',
            field=models.UUIDField(default=uuid.UUID('2e84749a-db61-4379-9aa6-12d48e471a94'), editable=False),
        ),
    ]
