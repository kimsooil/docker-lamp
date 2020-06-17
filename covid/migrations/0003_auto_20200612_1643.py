# Generated by Django 2.2.12 on 2020-06-12 20:43

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0009_auto_20200612_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='default_counties',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=80, verbose_name='County Name'), help_text='Default Counties', size=10),
        ),
    ]
