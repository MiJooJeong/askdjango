from django import forms
from .models import Post
from .models import GameUser


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['title', 'content', 'user_agent']
        widgets = {
            'user_agent': forms.HiddenInput,
        }

    '''
    def save(self, commit=True):
        post = Post(**self.cleaned_data)
        if commit:
            post.save()
        return post
    '''


class GameUserSignupForm(forms.ModelForm):
    class Meta:
        model = GameUser
        fields = ['server_name', 'username']

    def clean_username(self):
        # 값 변환은 clean 함수에서만 가능. validator는 지원하지 않음.
        return self.cleaned_data.get('username', '').strip()
