# Generated by Django 4.0.4 on 2022-07-17 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_remove_transactionmodel_payment_method_types_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositmodel',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending')], default='Pending', max_length=100),
        ),
    ]
