# Generated by Django 4.0.4 on 2022-07-17 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_transactionmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionmodel',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
