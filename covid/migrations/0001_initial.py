# Generated by Django 2.2.12 on 2020-04-28 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'State',
                'verbose_name_plural': 'States',
            },
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='County Name')),
                ('hospital_bed_capacity', models.IntegerField(blank=True, null=True, verbose_name='Hospital Bed Capacity')),
                ('icu_bed_capacity', models.IntegerField(blank=True, null=True, verbose_name='ICU Bed Capacity')),
                ('ventilator_capacity', models.IntegerField(blank=True, null=True, verbose_name='Ventilator Capacity')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covid.State', verbose_name='State')),
            ],
            options={
                'verbose_name': 'County',
                'verbose_name_plural': 'Counties',
            },
        ),
    ]
