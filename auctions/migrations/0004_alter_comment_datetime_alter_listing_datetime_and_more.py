# Generated by Django 5.0.3 on 2024-04-07 21:50

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_comment_datetime_alter_listing_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 7, 21, 50, 41, 495627, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 7, 21, 50, 41, 485884, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
