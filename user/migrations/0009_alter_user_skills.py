# Generated by Django 4.0.4 on 2022-05-16 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_reviews'),
        ('user', '0008_rename_user_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='skills',
            field=models.ManyToManyField(blank=True, to='projects.desiredexpertise'),
        ),
    ]
