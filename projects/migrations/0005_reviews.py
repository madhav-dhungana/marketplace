# Generated by Django 4.0.4 on 2022-05-13 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0004_alter_project_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('rating', models.IntegerField()),
                ('for_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('review_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_given', to=settings.AUTH_USER_MODEL)),
                ('review_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_got', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
