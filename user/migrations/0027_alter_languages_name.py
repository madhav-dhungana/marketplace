# Generated by Django 4.0.4 on 2022-06-25 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_alter_identityform_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languages',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]