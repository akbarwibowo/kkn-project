# Generated by Django 5.1 on 2024-09-04 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_alter_userextend_phone_alter_userextend_rt_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userextend',
            old_name='user_id',
            new_name='user',
        ),
    ]
