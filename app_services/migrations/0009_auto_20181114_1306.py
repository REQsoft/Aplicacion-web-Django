# Generated by Django 2.0.7 on 2018-11-14 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_services', '0008_auto_20181114_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='groups',
            field=models.ManyToManyField(to='app_services.Group'),
        ),
        migrations.AddField(
            model_name='menu',
            name='groups',
            field=models.ManyToManyField(to='app_services.Group'),
        ),
    ]