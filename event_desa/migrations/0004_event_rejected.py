# Generated by Django 5.1 on 2024-09-07 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_desa', '0003_event_event_time_alter_event_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]
