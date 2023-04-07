# Generated by Django 4.0.4 on 2022-05-16 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_verified_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Employer', 'Employer'), ('Freelancer', 'Freelancer')], default='Freelancer', max_length=200),
        ),
    ]