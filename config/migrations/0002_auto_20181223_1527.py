# Generated by Django 2.1.4 on 2018-12-23 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='folder',
            old_name='dbgroup',
            new_name='groups',
        ),
    ]
