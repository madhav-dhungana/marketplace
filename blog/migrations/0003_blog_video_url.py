# Generated by Django 4.0.4 on 2022-09-23 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_is_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]