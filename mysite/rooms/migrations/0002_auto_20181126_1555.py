# Generated by Django 2.1.3 on 2018-11-26 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='visibility',
            new_name='is_public',
        ),
    ]
