# Generated by Django 2.1.3 on 2018-11-08 23:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_services', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_admin', '0004_rol_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groups', models.ManyToManyField(related_name='get_groups', to='app_services.Group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='get_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
        migrations.RemoveField(
            model_name='rol',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='rol',
            name='user',
        ),
        migrations.DeleteModel(
            name='Rol',
        ),
    ]