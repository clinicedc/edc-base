# Generated by Django 2.0.7 on 2018-07-31 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edc_base', '0005_userprofile_print_server'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
