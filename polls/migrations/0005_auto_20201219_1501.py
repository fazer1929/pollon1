# Generated by Django 3.1.3 on 2020-12-19 09:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20201219_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 19, 15, 1, 7, 934914), verbose_name='Date Published'),
        ),
    ]