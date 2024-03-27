from django.contrib import admin

from audio_tribe.transcribe.models import Job
from audio_tribe.transcribe.models import UploadFile

# Register your models here.
admin.site.register(Job)
admin.site.register(UploadFile)
