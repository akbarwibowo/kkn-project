# Generated by Django 5.1 on 2024-09-08 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_alter_batch_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.batch')),
            ],
        ),
    ]
