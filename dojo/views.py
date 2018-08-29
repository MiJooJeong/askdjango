import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # 방법 1)
            '''
            post = Post()
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            '''

            # 방법 2)
            '''
            post = Post(title=form.cleaned_data['title'], 
                        content=form.cleaned_data['content'])
            post.save()
            '''

            # 방법 3)
            '''
            post = Post.objects.create(title=form.cleaned_data['title'],
                                       content=form.cleaned_data['content'])
            '''

            # 방법 4)
            post = form.save(commit=False)
            post.ip = request.META['REMOTE_ADDR']
            post.save()
            return redirect('/dojo/')   # namespace: name
    else:
        form = PostForm()
    return render(request, 'dojo/post_form.html', {
        'form': form,
    })


def mysum(request, numbers):
    # request: HttpRequest
    # result = sum(map(int, numbers.split('/')))
    result = sum(map(lambda s: int(s or 0), numbers.split('/')))
    return HttpResponse(result)


def hello(request, name, age):
    return HttpResponse('안녕하세요, {}. {}살이시네요'.format(name, age))


def post_list1(request):
    'FBV: 직접 문자열로 HTML 형식 응답하기'

    name = '공유'
    return HttpResponse('''
        <h1>AskDjango</h1>
        <p>{name}</p>
        <p>여러분의 파이썬&장고 페이스메이커가 되겠습니다.</p>
    '''.format(name=name))


def post_list2(request):
    'FBV: 템플릿을 통해 HTML 형식 응답하기'

    name = '공유'
    return render(request, "dojo/post_list.html", {'name': name})


def post_list3(request):
    'FBV: JSON 형식 응답하기'

    return JsonResponse({
        'message': '안녕, 파이썬&장고',
        'items': ['파이썬', '장고', 'Celery', 'Azure', 'AWS'],
    }, json_dumps_params={'ensure_ascii': False})


def excel_download(request):
    'FBV: 엑셀 다운로드 응답하기'

    # filepath = '/Users/joo/git/study/ask/django/askdjango/180607_SF_HLA.xls'
    filepath = os.path.join(settings.BASE_DIR, '180607_SF_HLA.xls')
    filename = os.path.basename(filepath)

    with open(filepath, 'rb') as f:
        response = HttpResponse(f, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response
