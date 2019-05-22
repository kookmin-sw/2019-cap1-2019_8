import time

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from .forms import DocumentForm
from .models import Document
import requests


class ProgressBarUploadView(View):
    def get(self, request):
        file_list = Document.objects.all()
        return render(self.request, 'Dream/progress_bar_upload/index.html', {'files': file_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = DocumentForm(self.request.POST, self.request.FILES)

        # send engine
        req = requests.post("http://localhost:8080/dream_upload", files={"file": self.request.FILES["file"]})
        if req.status_code == 200:
            result = req.json()
            if float(result["result"]["LightGBM"]) < 0.5:
                file = form.save()
                data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
            else:
                data = {'is_valid': False}
                print("Detected Malicious file")
        else:
            data = {'is_valid': False}
            print("ERROR")

        return JsonResponse(data)


def clear_database(request):
    for d_file in Document.objects.all():
        d_file.file.delete()
        d_file.delete()
    return redirect(request.POST.get('next'))



def my_view(request):
    return redirect('Dream:progress_bar_upload')
