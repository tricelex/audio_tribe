from django import forms

from audio_tribe.transcribe.models import Job


class JobCreationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["original_video", "target_language"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(JobCreationForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super(JobCreationForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
