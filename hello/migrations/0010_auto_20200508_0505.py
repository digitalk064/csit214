# Generated by Django 3.0.1 on 2020-05-08 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0009_auto_20200508_0412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='$ / hour', max_digits=6),
        ),
    ]
