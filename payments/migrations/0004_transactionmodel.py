# Generated by Django 4.0.4 on 2022-07-17 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0003_rename_account_linked_connectedfreelancer_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stripe_transaction_id', models.CharField(max_length=100, null=True)),
                ('type', models.CharField(choices=[('Transfer', 'Transfer'), ('Withdraw', 'Withdraw'), ('Payment', 'Payment'), ('Refund', 'Refund')], max_length=100)),
                ('status', models.CharField(choices=[('success', 'success'), ('rejected', 'rejected')], max_length=100)),
                ('transaction_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
