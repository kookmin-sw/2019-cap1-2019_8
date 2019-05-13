from django.views import View
from .models import Document
from django.core.paginator import Paginator
from django.shortcuts import render
from Dream.forms import PostSearchForm
from django.db.models import Q


class ProgressBarUploadView(View):
    def get(self, request):
        form = PostSearchForm()
        file_list = Document.objects.all()
        paginator = Paginator(file_list, 100)

        page = request.GET.get('page')
        items = paginator.get_page(page)

        context = {
            'files': items,
            'form': form,
            'result': False
        }
        return render(self.request, 'Dream/progress_bar_upload/index.html', context)

    def post(self, request):
        form = PostSearchForm()
        search_word = self.request.POST['search_word']
        # Post의 객체중 제목이나 설명이나 내용에 해당 단어가 대소문자관계없이(icontains) 속해있는 객체를 필터링
        # Q객체는 |(or)과 &(and) 두개의 operator와 사용가능
        post_list = Document.objects.filter(Q(title__icontains=search_word))

        context = {
            'search_term': search_word,
            'files': post_list,
            'form': form,
            'result': True,
            'count': len(post_list)
        }
        return render(self.request, 'Dream/progress_bar_upload/index.html', context)