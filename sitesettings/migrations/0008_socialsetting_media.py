# Generated by Django 4.0.4 on 2022-08-31 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitesettings', '0007_localizationsetting_othersetting_paymentsetting_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialsetting',
            name='media',
            field=models.CharField(choices=[('Google', 'Google'), ('Facebook', 'Facebook'), ('Twitter', 'Twitter'), ('Linkdin', 'Linkdin')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]