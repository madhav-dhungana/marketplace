# Generated by Django 4.0.4 on 2022-09-24 16:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_subscriber_alter_blog_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='token',
            field=models.UUIDField(default=uuid.UUID('ba98320a-8611-4622-810e-ed2bd207e417'), editable=False),
        ),
    ]
