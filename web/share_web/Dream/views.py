import time
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from .forms import DocumentForm
from .models import Document
from django.core.paginator import Paginator


class ProgressBarUploadView(View):
    def get(self, request):
        file_list = Document.objects.all()
        paginator = Paginator(file_list, 5)

        page = request.GET.get('page')
        items = paginator.get_page(page)

        context = {
            'files': items
        }
        return render(self.request, 'Dream/progress_bar_upload/index.html', context)

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = DocumentForm(self.request.POST, self.request.FILES)
        print(type(self.request.POST))
        if form.is_valid():
            file = form.save()
            data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
        else:
            data = {'is_valid': False}

        return JsonResponse(data)


def clear_database(request):
    for d_file in Document.objects.all():
        d_file.file.delete()
        d_file.delete()
    return redirect(request.POST.get('next'))
