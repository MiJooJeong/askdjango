from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Comments, Tag


# 등록법 1
# admin.site.register(Post) # 기본 ModelAdmin으로 등록


# 등록법 2
# class PostAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'created_at', 'updated_at']
#
# admin.site.register(Post, PostAdmin) # 참고: 같은 모델 중복 등록은 불가


# 등록법 3 : 장식자 형태로 지원
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'tag_list', 'content_size', 'status', 'created_at', 'updated_at']
    actions = ['make_draft', 'make_published']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('tag_set')

    def tag_list(self, post):
        return ', '.join(tag.name for tag in post.tag_set.all())    # list comprehension

    def content_size(self, post):
        return mark_safe('<strong>{}</strong>글자'.format(len(post.content)))

    content_size.short_description = '글자수'
    # content_size.allow_tags = True  # Deprecated

    def make_published(self, request, queryset):
        updated_count = queryset.update(status='p')  # QuerySet.update
        self.message_user(request, '{}건의 포스팅을 Published 상태로 변경'.format(updated_count))  # django message framework 활용

    make_published.short_description = '지정 포스팅을 Published 상태로 변경합니다.'

    def make_draft(self, request, queryset):
        updated_count = queryset.update(status='d')  # QuerySet.update
        self.message_user(request, '{}건의 포스팅을 Draft 상태로 변경'.format(updated_count))  # django message framework 활용

    make_draft.short_description = '지정 포스팅을 Draft 상태로 변경합니다.'


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post_content_len']
    # list_select_related = ['post']

    def post_content_len(self, comment):
        return '{}글자'.format(len(comment.post.content))

    def get_queryset(self, request):
        qs = super().get_queryset()
        return qs.select_related('post')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']