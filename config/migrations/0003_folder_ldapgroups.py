# Generated by Django 2.1.4 on 2018-12-23 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20181223_1521'),
        ('config', '0002_auto_20181223_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='ldapgroups',
            field=models.ManyToManyField(blank=True, to='main.LDAPGroup'),
        ),
    ]
