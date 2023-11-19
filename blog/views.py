from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView
from database.models import articles
# Create your views here.

class IndexView(TemplateView):
    template_name = 'blog/index.html'
    title = 'Онлайн-Кинотеатр'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        d = super().get_context_data(**kwargs)
        d['title'] = self.title
        x = articles.objects.raw('SELECT * FROM database_articles ORDER BY id DESC LIMIT 3')
        # x = x.__dict__
        lst = []
        for elem in x:
            print(elem.__dict__)
            lst.append((elem.__dict__['id'], elem.__dict__['title'], elem.__dict__['date']))
        print(lst)
        d['aritcles'] = lst
        return d
    
from django.core.paginator import Paginator
from django.shortcuts import render
from database.models import articles
from cinema import settings
import os
from django.http import FileResponse, Http404
from database.models import articles, films, genre, member_film, info, comments, prev_next_comm, favorites, history, rating, prev_next_comm, user, rating
from django.core.paginator import Paginator
from django.shortcuts import render
from database.models import articles, films, genre, member_film, info, comments, prev_next_comm, favorites, history, rating, prev_next_comm, user, rating
# from blog.forms import Commentform
from cinema import settings
import os
from django.http import FileResponse

def blog(request):
    lst = []
    name = ''
    if request.method == 'POST':
        dict_of_post = dict(request._post)
        for key, value in dict_of_post.items():
            if value[0] == 'on':
                lst.append(key)
            if key == 'name':
                name += value[0]
    blog_list = []
    if name != '':
        name = '%' + name + '%'
        blog_list_tmp = articles.objects.raw(
            'SELECT database_articles.id as id, database_articles.date, database_articles.path, database_articles.title'
            ' FROM database_articles WHERE database_articles.title LIKE = %s',[name, ])
        for elem in blog_list_tmp:
            e = elem.__dict__
            blog_list.append((e['id'], e['id_author'], e['date'], e['path'],e['title']))
    else:
        pass
    if request.method != 'POST':
        blog_list_tmp = articles.objects.raw(
            'SELECT database_articles.id, database_user.username, database_articles.date, database_articles.path, '
            'database_articles.title  FROM database_articles INNER JOIN database_user ON database_articles.id_author_id = database_user.id')
        for elem in blog_list_tmp:
            e = elem.__dict__
            blog_list.append((e['id'], e['username'], e['date'], e['path'], e['title']))

    paginator = Paginator(blog_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'title':'Блог',
        'articles': blog_list,
        'page_obj': page_obj
    }

    return render(request, 'blog/index_b.html', context)


def article_id(request, article_id):
    article_list = articles.objects.raw(
        'SELECT database_articles.id, database_user.username, database_articles.date, database_articles.path, '
            'database_articles.title  FROM database_articles INNER JOIN database_user ON database_articles.id_author_id = database_user.id WHERE database_articles.id = %s',
        [article_id, ])
    if len(article_list) == 0:
        context = {
            'title': 'Ошибка',
            'text': 'Такой новостной статьи не существует',

        }
        return render(request, 'blog/fail.html', context)
    article_list_x = []
    for elem in article_list:
        e = elem.__dict__
        article_list_x.append((e['id'], e['username'], e['date'], e['path'], e['title']))
    author = article_list_x[0][1]
    date = article_list_x[0][2]
    path = article_list_x[0][3]
    title = article_list_x[0][4]
    fl = 0
    context = {
        'id': article_id,
        'author': author,
        'date': date,
        'path':'../../media/' + path,
        'title': title

    }
    if request.method == 'POST':
        form = Commentform(request.POST)
        context['form'] = form
        k = list(request._post.keys())
        if 'text_com' in k:
            x = user.objects.filter(username=str(request.user))
            id = 1
            for elem in x:
                e = elem.__dict__
                id = e['id']
            s = request._post['text_com']
            if 'id_com' in k:
                x = str(request._post['id_com'])
                if x != '':
                    s += ' Ответный комментарий на ' + str(request._post['id_com'])

            com = comments(text=s, id_author_id=id)

            com.save()
            if 'id_com' in k:
                x = str(request._post['id_com'])
                if x != '':
                    con = prev_next_comm(id_child_id=com.id, id_parent_id=request._post['id_com'])
                    con.save()
            rat = rating(id_author_id=id, id_of_art_film=context['id'], id_content_id=com.id, rating=request._post['ra'],
                         context='article')
            rat.save()
        id = article_list_x[0][0]
        rates_list = rating.objects.raw(
            'SELECT 1 as id, id_content_id, rating, text from database_rating INNER JOIN database_comments on database_rating.id_content_id = database_comments.id WHERE context=%s AND id_of_art_film = %s',
            ['article', id])
        rate_l = []

        for elem in rates_list:
            e = elem.__dict__
            rate_l.append((e['id_content_id'], e['text'], e['rating']))

        context['comment_list'] = rate_l

    return render(request, 'blog/article.html', context)

def pdf_view(request,article_id):
    article_list = articles.objects.raw(
        'SELECT database_articles.id, database_articles.path FROM database_articles WHERE database_articles.id = %s',
        [article_id, ])
    article_list_x = []
    for elem in article_list:
        e = elem.__dict__
        article_list_x.append((e['id'],e['path']))
    path = article_list_x[0][1]
    filepath = os.path.join(settings.MEDIA_ROOT, path)
    print(filepath)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')