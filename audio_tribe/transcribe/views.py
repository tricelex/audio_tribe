from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic

from audio_tribe.transcribe.forms import JobCreationForm
from audio_tribe.transcribe.models import Job
from audio_tribe.transcribe.models import UploadFile
from audio_tribe.transcribe.tasks import initiate_transcription_task

# Create your views here.


class UploadView(generic.CreateView):
    template_name = "transcribe/upload.html"
    model = UploadFile
    fields = ["file"]

    def get_success_url(self):
        return reverse("transcribe:upload")

    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)
        context.update(
            {
                "uploads": UploadFile.objects.all(),
            }
        )
        return context


class JobsListView(generic.ListView):
    template_name = "transcribe/job.html"
    model = Job
    context_object_name = "jobs"
    form_class = JobCreationForm
    success_url = reverse_lazy("transcribe:job")

    def get_success_url(self):
        # return reverse_lazy('transcribe:job')
        return reverse("transcribe:job")

    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None
        return Job.objects.filter(user=user).order_by("-created_datetime")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(
            user=self.request.user
        )  # Pass the user to the form
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.POST, request.FILES, user=request.user
        )  # Pass the user to the form
        if form.is_valid():
            form.save()
            initiate_transcription_task.delay(form.instance.id)
            return render(
                request, self.template_name, {"form": form, "jobs": self.get_queryset()}
            )
        else:
            return render(
                request, self.template_name, {"form": form, "jobs": self.get_queryset()}
            )

    def form_valid(self, form):
        return super().form_valid(form)
