# Generated by Django 2.0.7 on 2018-11-14 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_services', '0012_auto_20181114_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='service',
            new_name='services',
        ),
    ]