# Generated by Django 5.1 on 2024-09-08 13:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_alter_batch_input_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='batch',
            name='date',
            field=models.DateField(default=datetime.date(2024, 9, 8)),
        ),
        migrations.AddField(
            model_name='batch',
            name='revision',
            field=models.BooleanField(default=False),
        ),
    ]
