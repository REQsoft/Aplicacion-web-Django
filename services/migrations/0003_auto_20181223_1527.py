# Generated by Django 2.1.4 on 2018-12-23 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20181223_1521'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='dbgroups',
            new_name='groups',
        ),
    ]