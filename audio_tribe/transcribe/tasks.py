from audio_tribe.transcribe.models import Job
from audio_tribe.transcribe.utils import transcode_video_to_audio
from config.celery_app import app


@app.task(name="initiate_transcription_task")
def initiate_transcription_task(job_id: str) -> None:
    """
    Initiates transcription task for an audio file
    """
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        print("Job does not exist")
        return

    # transcode the video file to audio
    print(f"Transcoding video file to audio for job: {job.id}")
    original_audio = transcode_video_to_audio(job.original_video.url)
    job.original_audio = original_audio
    job.save(update_fields=["original_audio"])

    print(f"Initiating transcription task for job: {job.id}")
