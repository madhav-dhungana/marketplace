# Generated by Django 4.0.4 on 2022-06-25 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_remove_notification_action_to_notification_action_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='user_has_seen',
            field=models.BooleanField(default=False),
        ),
    ]
