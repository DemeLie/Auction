# Generated by Django 5.0.3 on 2024-04-08 10:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_comment_datetime_alter_listing_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 8, 10, 4, 20, 979715, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 8, 10, 4, 20, 968716, tzinfo=datetime.timezone.utc)),
        ),
    ]
