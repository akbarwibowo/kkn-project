# Generated by Django 5.1 on 2024-09-07 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_desa', '0004_event_rejected'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventmessage',
            old_name='information',
            new_name='event',
        ),
    ]
