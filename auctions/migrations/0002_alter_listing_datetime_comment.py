# Generated by Django 5.0.3 on 2024-04-07 20:59

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 7, 20, 59, 34, 475676, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=255)),
                ('datetime', models.DateTimeField(default=datetime.datetime(2024, 4, 7, 20, 59, 34, 486691, tzinfo=datetime.timezone.utc))),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]