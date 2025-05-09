# Generated by Django 5.1.5 on 2025-04-16 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_alter_appointment_options_and_more'),
        ('cases', '0003_case_description_case_status_alter_case_client'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['-date_time']},
        ),
        migrations.AddField(
            model_name='appointment',
            name='case',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='cases.case'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('SCHEDULED', 'Scheduled'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled'), ('RESCHEDULED', 'Rescheduled')], default='SCHEDULED', max_length=20),
        ),
    ]
