from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.

class IndexView(TemplateView):
    template_name = 'blog/index.html'
    title = 'Store'
    
from django.core.paginator import Paginator
from django.shortcuts import render
from database.models import articles
from cinema import settings
import os
from django.http import FileResponse, Http404


def blog(request):
    dict_of_post = {}
    lst = []
    name = ''
    if request.method == 'POST':
        dict_of_post = dict(request._post)
        # print(dict_of_post)
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
            'SELECT database_articles.id as id, database_articles.date, database_articles.path, database_articles.title  FROM database_articles')
        for elem in blog_list_tmp:
            e = elem.__dict__
            blog_list.append((e['id'], e['date'], e['path'],e['title']))

    paginator = Paginator(blog_list, 3)
    #print(paginator.count, ' ', paginator.num_pages)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'title':'Блог',
        'articles': blog_list,
        'page_obj': page_obj
    }
    return render(request, 'blog/index_b.html', context)

def display(request):
     return render(request,"blog/test.html", {"objects": "bar"})


def article_id(request, article_id):
    article_list = articles.objects.raw(
        'SELECT database_articles.id, database_articles.date, database_articles.path, database_articles.title'
        ' FROM database_articles WHERE database_articles.id = %s',
        [article_id, ])
    article_list_x = []
    for elem in article_list:
        e = elem.__dict__
        article_list_x.append((e['id'],  e['date'], e['path'], e['title']))
    date = article_list_x[0][1]
    path = article_list_x[0][2]
    title = article_list_x[0][3]
    context = {
        'id': article_id,
        'date': date,
        'path':'../../media/' + path,
        'title': title

    }
    if request.method == 'POST':
        print('post')
    return render(request, 'blog/article.html', context)

def pdf_view(request,article_id):
    article_list = articles.objects.raw(
        'SELECT database_articles.id, database_articles.date, database_articles.path, database_articles.title'
        ' FROM database_articles WHERE database_articles.id = %s',
        [article_id, ])
    article_list_x = []
    for elem in article_list:
        e = elem.__dict__
        article_list_x.append((e['id'], e['date'], e['path'], e['title']))
    path = article_list_x[0][2]
    filepath = os.path.join(settings.MEDIA_ROOT, path)
    print(filepath)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')