import uuid

from django.db import models

from audio_tribe.libs.base_model import BaseAbstractModel
from audio_tribe.transcribe.enums import JobStatus
from audio_tribe.transcribe.enums import LanguageChoices
from audio_tribe.users.models import User


# Create your models here.
class UploadFile(BaseAbstractModel):
    file = models.FileField(upload_to="uploads/")

    def __str__(self):
        return self.file.name


class Job(BaseAbstractModel):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    original_video = models.FileField(
        upload_to="original_videos/", null=True, blank=True
    )
    original_audio = models.FileField(
        upload_to="original_audios/", null=True, blank=True
    )
    source_language = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=JobStatus.choices(),
        default=JobStatus.PENDING.choice_value,
    )
    target_language = models.CharField(
        max_length=50, choices=LanguageChoices.choices(), null=True, blank=True
    )
    transcript = models.JSONField(null=True, blank=True)
    transcription_id = models.CharField(max_length=50, null=True, blank=True)
    translated_audio = models.FileField(
        upload_to="translated_audios/", null=True, blank=True
    )
    translated_text = models.TextField(null=True, blank=True)

    video_url = models.URLField(null=True, blank=True)
    voice_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"ID: {self.id} - Target Language: {self.target_language} - Status: {self.status}"
