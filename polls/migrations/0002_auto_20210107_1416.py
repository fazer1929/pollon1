# Generated by Django 3.1.3 on 2021-01-07 08:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 7, 14, 16, 54, 718542), verbose_name='Date Published'),
        ),
    ]