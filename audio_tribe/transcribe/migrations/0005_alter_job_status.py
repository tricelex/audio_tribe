# Generated by Django 4.2.10 on 2024-03-27 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcribe', '0004_alter_job_target_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('uploading', 'Uploading'), ('transcribing', 'Transcribing'), ('translating', 'Translating'), ('cloning', 'Cloning'), ('synthesizing', 'Synthesizing'), ('synchronizing', 'Synchronizing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=50),
        ),
    ]
