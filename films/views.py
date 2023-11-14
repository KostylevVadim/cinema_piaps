from typing import Any
from django.shortcuts import render
from django.views.generic.list import ListView
from database.models import films, genre, member_film, info, comments, prev_next_comm, favorites, history, rating
from django.core.paginator import Paginator
from django.db import connection
    
def film(request):
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
        
        
    film_list = []
    if name != '':
        name = '%'+ name + '%'
        film_list_tmp = films.objects.raw('SELECT database_films.id as id,database_films.title, database_films.path, database_films.rating FROM database_films WHERE database_films.title LIKE %s', [name,])
        for elem in film_list_tmp:
                e =elem.__dict__
                
                film_list.append((e['id'],e['title'], e['path'], e['rating']))
    else:
        pass
    if len(lst)!=0 and name == '':
        ids = []
        for name in lst:
            g_ids = genre.objects.raw('SELECT 1 as id, database_genre.id as genre_id from database_genre WHERE database_genre.name = %s', [name,])
            # ids = []
            for el in g_ids:
                ids.append(el.__dict__['genre_id'])
        # print(ids)
        
        for id in ids:
            film_list_tmp = films.objects.raw('SELECT  database_films.id as id,database_films.title, database_films.path, database_films.rating FROM database_genre_films INNER JOIN database_films ON database_films.id = database_genre_films.films_id WHERE database_genre_films.genre_id = %s', [id,])
            for elem in film_list_tmp:
                e =elem.__dict__
                
                film_list.append((e['id'],e['title'], e['path'], e['rating']))
    if request.method != 'POST':
        film_list_tmp = films.objects.raw('SELECT database_films.id as id,database_films.title, database_films.path, database_films.rating FROM database_films')
        for elem in film_list_tmp:
                e =elem.__dict__
                
                film_list.append((e['id'],e['title'], e['path'], e['rating']))

    
    
    genre_list = genre.objects.all()
    

    paginator = Paginator(film_list, 3)
    print(paginator.count, ' ',paginator.num_pages)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title':'Кинотеатр',
        'films': film_list,
        'genre': genre_list,
        'page_obj': page_obj
        
    }
    return render(request,'films/films.html', context)

def film_id(request, film_id):
    films_list = films.objects.raw('SELECT database_films.id as id,database_films.title, database_films.path, database_films.rating FROM database_films WHERE database_films.id = %s', [film_id,])
    genre = []
    film_list_x = []
    for elem in films_list:
        e =elem.__dict__
        film_list_x.append((e['id'],e['title'], e['path'], e['rating']))
    title = film_list_x[0][1]
    path = film_list_x[0][2]
    rating = film_list_x[0][3]
    
    context = {
        'title':title,
        'path': path,
        'rating': rating
        
    }
    if request.method == 'POST':
        print('post')
    return render(request,'films/film.html', context)
