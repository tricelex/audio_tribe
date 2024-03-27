from django.urls import path

from audio_tribe.transcribe.views import JobsListView
from audio_tribe.transcribe.views import UploadView

app_name = "transcribe"
urlpatterns = [
    path("", view=UploadView.as_view(), name="upload"),
    path("jobs/", view=JobsListView.as_view(), name="job"),
]
