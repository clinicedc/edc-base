# Generated by Django 2.0.1 on 2018-01-17 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("edc_base", "0004_auto_20180115_0030")]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="print_server",
            field=models.CharField(
                blank=True,
                help_text='Change in <a href="/edc_label/">Edc Label Administration</a>',
                max_length=100,
                null=True,
            ),
        )
    ]
