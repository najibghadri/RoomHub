# Generated by Django 2.1.3 on 2018-11-26 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0009_event_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(verbose_name='End'),
        ),
    ]
