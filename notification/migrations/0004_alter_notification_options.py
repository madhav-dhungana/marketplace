# Generated by Django 4.0.4 on 2022-06-26 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_notification_user_has_seen'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-id']},
        ),
    ]
