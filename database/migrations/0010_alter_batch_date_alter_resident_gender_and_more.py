# Generated by Django 5.1 on 2024-09-15 07:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_alter_resident_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='date',
            field=models.DateField(default=datetime.date(2024, 9, 15)),
        ),
        migrations.AlterField(
            model_name='resident',
            name='gender',
            field=models.CharField(choices=[('laki-laki', 'laki-laki'), ('perempuan', 'perempuan')], max_length=10),
        ),
        migrations.AlterField(
            model_name='resident',
            name='work',
            field=models.CharField(default='tidak bekerja', max_length=15),
        ),
    ]
