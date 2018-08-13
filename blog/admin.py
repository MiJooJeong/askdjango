from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post


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
    list_display = ['id', 'title', 'content_size', 'created_at', 'updated_at']

    def content_size(self, post):
        return mark_safe('<strong>{}</strong>글자'.format(len(post.content)))

    content_size.short_description = '글자수'
    # content_size.allow_tags = True  # Deprecated