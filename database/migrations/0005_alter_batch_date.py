# Generated by Django 5.1 on 2024-09-08 14:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_alter_batch_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='date',
            field=models.DateField(default=datetime.date(2024, 9, 8)),
        ),
    ]
