# Generated by Django 4.1.1 on 2023-05-16 09:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeitem',
            name='date_of',
            field=models.DateField(default=datetime.date.today),
        ),
    ]