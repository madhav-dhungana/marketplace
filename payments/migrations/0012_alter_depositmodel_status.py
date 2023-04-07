# Generated by Django 4.0.4 on 2022-07-17 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0011_alter_depositmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositmodel',
            name='status',
            field=models.CharField(choices=[('Released', 'Released'), ('On Hold', 'On Hold')], default='On Hold', max_length=100),
        ),
    ]
