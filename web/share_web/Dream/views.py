from django.shortcuts import render, redirect
from django.views import View
from .models import Document
from django.core.paginator import Paginator


class ProgressBarUploadView(View):
    def get(self, request):
        file_list = Document.objects.all()
        paginator = Paginator(file_list, 100)

        page = request.GET.get('page')
        items = paginator.get_page(page)

        context = {
            'files': items
        }
        return render(self.request, 'Dream/progress_bar_upload/index.html', context)