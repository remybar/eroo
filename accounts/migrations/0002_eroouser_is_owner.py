# Generated by Django 3.1.13 on 2021-10-08 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eroouser',
            name='is_owner',
            field=models.BooleanField(default=False),
        ),
    ]
