# Generated by Django 4.0.4 on 2022-07-19 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_alter_project_employer_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='employer_payment_status',
            field=models.CharField(blank=True, choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid'), ('Refunded', 'Refunded')], default='Unpaid', max_length=20),
        ),
    ]
