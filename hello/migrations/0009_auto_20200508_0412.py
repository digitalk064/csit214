# Generated by Django 3.0.1 on 2020-05-08 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0008_auto_20200508_0410'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='user',
            new_name='booker',
        ),
    ]
