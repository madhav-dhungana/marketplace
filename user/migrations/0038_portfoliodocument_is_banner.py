# Generated by Django 4.0.4 on 2022-09-27 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0037_portfoliodocument_portfolio'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfoliodocument',
            name='is_banner',
            field=models.BooleanField(default=False),
        ),
    ]
