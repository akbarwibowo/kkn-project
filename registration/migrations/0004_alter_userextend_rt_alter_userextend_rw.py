# Generated by Django 5.1 on 2024-09-07 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_rename_user_id_userextend_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextend',
            name='rt',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='userextend',
            name='rw',
            field=models.SmallIntegerField(),
        ),
    ]
