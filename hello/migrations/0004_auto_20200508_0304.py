# Generated by Django 3.0.1 on 2020-05-08 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_auto_20200508_0223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='user',
            new_name='staff',
        ),
    ]
