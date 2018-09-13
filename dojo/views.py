import os

from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DetailView

from .forms import PostForm
from .models import Post

# # STEP 1. FBV 버전
# def post_detail(request, id):
#     post = get_object_or_404(Post, id=id)
#     return render(request, 'dojo/post_detail.html', {
#         'post': post,
#     })


# # STEP 2. 함수를 통해 view 생성 버전
# def generate_view_fn(model):
#     def view_fn(request, id):
#         instance = get_object_or_404(model, id=id)
#         instance_name = model._meta.model_name
#         template_name = '{}/{}_detail.html'.format(model._meta.app_label, instance_name)
#         return render(request, template_name, {
#             instance_name: instance,
#         })
#     return view_fn
#
#
# post_detail = generate_view_fn(Post)


# # STEP 3. CBV 형태로 컨셉만 구현한 버전
# class DetailView(object):
#     """
#     이전 FBV를 CBV 버전으로 컨셉만 간단히 구현. 같은 동작은 수행
#     """
#
#     def __init__(self, model):
#         self.model = model
#
#     def get_object(self, *args, **kwargs):
#         return get_object_or_404(self.model, id=kwargs['id'])
#
#     def get_template_name(self):
#         return '{}/{}_detail.html'.format(self.model._meta.app_label, self.model._meta.model_name)
#
#     def dispatch(self, request, *args, **kwargs):
#         return render(request, self.get_template_name(), {
#             self.model._meta.model_name: self.get_object(*args, **kwargs),
#         })
#
#     @classmethod
#     def as_view(cls, model):
#         def view(request, *args, **kwargs):
#             self = cls(model)
#             return self.dispatch(request, *args, **kwargs)
#         return view
#
#
# post_detail = DetailView.as_view(Post)


# STEP 4. django 기본 제공 DetailView CBV 쓰기
post_detail = DetailView.as_view(model=Post)


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


def post_edit(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.ip = request.META['REMOTE_ADDR']
            post.save()
            return redirect('/dojo/')   # namespace: name
    else:
        form = PostForm(instance=post)
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
