# Generated by Django 3.0.1 on 2020-05-08 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_auto_20200508_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]