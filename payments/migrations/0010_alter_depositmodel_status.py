# Generated by Django 4.0.4 on 2022-07-17 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_depositmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositmodel',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('On Hold', 'On Hold')], default='Pending', max_length=100),
        ),
    ]
