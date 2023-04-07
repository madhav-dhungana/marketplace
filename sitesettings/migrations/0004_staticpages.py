# Generated by Django 4.0.4 on 2022-07-25 15:15

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitesettings', '0003_alter_sitesetting_favicon_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_agrement', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='User Agrement')),
                ('privacy_policy', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Privacy Policies')),
                ('cookie_policies', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Cookie Policies')),
            ],
        ),
    ]