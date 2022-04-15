from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail

from blog.forms import EmailPostForm
from .models import Post


# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginator_by = 3
    template_name = 'blog/post/list.html'


"""
Post list на обработчике функции 

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # По 3 статьи на каждой странице.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее кол-чи страниц, возвращаем последнюю.
        posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})
"""


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    # Получение статьи по идентификатору.
    post = get_object_or_404(Post, id=post_id, status='published')
    send = False 

    if request.method == 'POST':
        # Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию.
            cd = form.cleaned_data
            # Отправка электронной почтой
            post_url = request.build_absolute_url(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(
                cd['name', cd['email'], post.title])
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message,
                      'frombohdankovalsup@gmail.com', [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'post': post, 'form': form})

