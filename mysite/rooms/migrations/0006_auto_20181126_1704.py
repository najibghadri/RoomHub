# Generated by Django 2.1.3 on 2018-11-26 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_auto_20181126_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_start',
            field=models.DateTimeField(verbose_name='Event start'),
        ),
    ]