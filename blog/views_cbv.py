from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .models import Post


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all().prefetch_related('tag_set', 'comments_set')
    paginate_by = 10
    

post_list = PostListView.as_view()

post_detail = DetailView.as_view(model=Post)

post_new = CreateView.as_view(model=Post)

post_edit = UpdateView.as_view(model=Post, fields='__all__')

post_delete = DeleteView.as_view(model=Post, success_url=reverse_lazy('blog:post_list'))
