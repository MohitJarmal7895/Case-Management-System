# Generated by Django 5.2 on 2025-04-27 14:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0005_case_assigned_attorney_alter_case_case_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='court_name',
            field=models.CharField(default='District Court', max_length=50),
        ),
        migrations.AddField(
            model_name='case',
            name='filing_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='case',
            name='description',
            field=models.TextField(default=' '),
        ),
    ]
