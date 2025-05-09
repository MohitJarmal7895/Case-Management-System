# Generated by Django 5.1.5 on 2025-04-16 07:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_remove_case_assigned_attorney_and_more'),
        ('documents', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ['-uploaded_at']},
        ),
        migrations.RenameField(
            model_name='document',
            old_name='created_at',
            new_name='uploaded_at',
        ),
        migrations.RemoveField(
            model_name='document',
            name='document_type',
        ),
        migrations.RemoveField(
            model_name='document',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='document',
            name='case',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='cases.case'),
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='document',
            name='uploaded_by',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
