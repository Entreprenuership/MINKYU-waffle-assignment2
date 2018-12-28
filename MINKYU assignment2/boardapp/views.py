from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['제목', '작성자', '내용', '비번']
        widgets = {
            '비밀번호': forms.PasswordInput,
        }

        def clean_password(self):
            password = self.cleaned_data['비번']
            if self.instance.pk:
                if password != self.instance.password:
                    raise ValidationError("땡!.", code='wrong_password')
            return password

class PostListView(ListView):
    model = Post
    paginate_by = 5

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm()

    def get_success_url(self):
        return reverse('post_detail', args = [self.object.pk])

class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.viewCnt += 1
        self.object.save()
        context = self.get_context_data(object = self.object)
        return self.render_to_response(context)

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm()

    def get_success_url(self):
        return reverse('post_detail', args = [self.object.pk])

class PostDeleteView(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('post_list')

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        if object.password != request.POST.get('비밀번호', ''):
            messages.error(request, '비밀번호 틀렸습니다;;')
            return HttpResponseRedirect(
                    reverse(args=[object.pk]))

        messages.info(request, '지워짐~ 지우개로 널 지울수만 있다면~')
        return super().post(self, request, *args, **kwargs)



#recommendCnt 뷰를 못 구현함 ㅜㅜ 일찍 시작할걸