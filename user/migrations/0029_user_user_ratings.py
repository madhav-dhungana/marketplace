# Generated by Django 4.0.4 on 2022-07-04 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0028_user_availability_weekdayavailable'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_ratings',
            field=models.FloatField(blank=True, null=True),
        ),
    ]