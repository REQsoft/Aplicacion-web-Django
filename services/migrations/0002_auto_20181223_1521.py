# Generated by Django 2.1.4 on 2018-12-23 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20181223_1521'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='groups',
        ),
        migrations.AddField(
            model_name='service',
            name='dbgroups',
            field=models.ManyToManyField(blank=True, to='main.DBGroup'),
        ),
        migrations.AddField(
            model_name='service',
            name='ldapgroups',
            field=models.ManyToManyField(blank=True, to='main.LDAPGroup'),
        ),
    ]
