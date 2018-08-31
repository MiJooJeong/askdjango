from django.contrib import admin
from .models import Post
from .models import GameUser


admin.site.register(Post)

admin.site.register(GameUser)