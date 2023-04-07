# Generated by Django 4.0.4 on 2022-10-11 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0003_extra_data_default_dict'),
        ('sitesettings', '0012_custommodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialApplication',
            fields=[
                ('socialapp_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='socialaccount.socialapp')),
                ('is_active', models.BooleanField(default=True)),
            ],
            bases=('socialaccount.socialapp',),
        ),
        migrations.DeleteModel(
            name='CustomModel',
        ),
    ]