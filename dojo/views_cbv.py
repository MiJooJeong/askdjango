import os
from django.views.generic import View, TemplateView
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from askdjango.settings import BASE_DIR


class PostListView1(View):
    'CBV: 직접 문자열로 HTML 형식 응답하기'

    def get(self, request):
        name = '공유'
        html = self.get_template_string().format(name=name)
        return HttpResponse(html)

    def get_template_string(self):
        return '''
            <h1>AskDjango</h1>
            <p>{name}</p>
            <p>여러분의 파이썬&장고 페이스메이커가 되겠습니다.</p>
        '''


post_list1 = PostListView1.as_view()


class PostListView2(TemplateView):
    'CBV: 템플릿을 통해 HTML 형식 응답하기'

    template_name = 'dojo/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['name'] = '공유'
        return context


post_list2 = PostListView2.as_view()


class PostListView3(View):
    'CBV: JSON 형식 응답하기'

    def get(self, request):
        return JsonResponse(self.get_data(), json_dumps_params={'ensure_ascii': False})

    def get_data(self):
        return {
            'message': '안녕, 파이썬&장고',
            'items': ['파이썬', '장고', 'Celery', 'Azure', 'AWS'],
        }


post_list3 = PostListView3.as_view()


class ExcelDownloadView(View):
    'CBV: 엑셀 다운로드 응답하기'

    filepath = os.path.join(BASE_DIR, '180607_SF_HLA.xls')

    def get(self, request):
        filename = os.path.basename(self.filepath)
        with open(filename, 'rb') as f:
            response = HttpResponse(f, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
            return response


excel_download = ExcelDownloadView.as_view()