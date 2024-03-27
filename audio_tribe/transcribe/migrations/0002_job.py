# Generated by Django 4.2.10 on 2024-03-24 05:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transcribe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_datetime', models.DateTimeField(auto_now=True, verbose_name='Last update at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('original_video', models.FileField(null=True, upload_to='original_videos/')),
                ('original_audio', models.FileField(null=True, upload_to='original_audios/')),
                ('source_language', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('target_language', models.CharField(max_length=50, null=True)),
                ('transcript', models.JSONField(null=True)),
                ('transcription_id', models.CharField(max_length=50, null=True)),
                ('translated_audio', models.FileField(null=True, upload_to='translated_audios/')),
                ('translated_text', models.TextField(null=True)),
                ('video_url', models.URLField(null=True)),
                ('voice_id', models.CharField(max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
