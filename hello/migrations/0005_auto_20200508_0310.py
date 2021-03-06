# Generated by Django 3.0.1 on 2020-05-08 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_auto_20200508_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(help_text='Maximum number of persons'),
        ),
        migrations.AlterField(
            model_name='room',
            name='img',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='room',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='$ / hour', max_digits=4),
        ),
    ]
