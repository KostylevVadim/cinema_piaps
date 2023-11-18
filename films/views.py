from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import ListView
from database.models import films, genre, member_film, info, comments, prev_next_comm, favorites, history, rating, prev_next_comm, user, rating
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from films.forms import Commentform
from django.shortcuts import render,HttpResponse
import datetime

list_to_save_dict ={}
@login_required
def film(request):
    dict_of_post = {}
    # if()
    lst = []
    name = ''
    key_list = list()
    
    if request.method == 'POST':
        list_to_save_dict.clear()
        dict_of_post = dict(request._post)
        print(dict_of_post)
        for key, value in dict_of_post.items():
            print(value[0])
            if value[0] == 'on':
                lst.append(key)
                list_to_save_dict[key]= ''
            
            if key == 'name':
                name += value[0] 
        
    # print(list_to_save_dict)
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
        # print(list_to_save_dict)
        
        s = ''
        for key, value in list_to_save_dict.items():
            s+=key
        
            film_list_tmp = films.objects.raw('SELECT database_films.id as id,database_films.title, database_films.path, database_films.rating FROM database_films INNER JOIN database_genre_films ON database_genre_films.films_id = database_films.id INNER JOIN database_genre ON database_genre.id = database_genre_films.genre_id WHERE database_genre.name = %s', [key,])
            for elem in film_list_tmp:
                    e =elem.__dict__
                
                    film_list.append((e['id'],e['title'], e['path'], e['rating']))

    
    
    genre_list = genre.objects.all()
    genre_list_new = []

    # print(list_to_save_dict)
    for elem in genre_list:
        # print(elem.__dict__['name'])
        if elem.__dict__['name'] in list_to_save_dict:
            # print(elem.__dict__['name'], '')
            genre_list_new.append((elem.__dict__['name'], 'checked'))
        else:
            # print(elem.__dict__['name'], 'disabled')
            genre_list_new.append((elem.__dict__['name'], ''))
    print(genre_list_new)
    paginator = Paginator(film_list, 3)
    # print(paginator.count, ' ',paginator.num_pages)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title':'Кинотеатр',
        'films': film_list,
        'genre': genre_list_new,
        'page_obj': page_obj
        
    }
    return render(request,'films/films.html', context)



@login_required
def film_id(request, film_id):
    # print(request.user.__dict__['_wrapped'].__dict__)
    x = user.objects.filter(username = str(request.user))
    id = 1
    for elem in x:
        e =elem.__dict__
        id =e['id']
    # print(id)
    id_u = id
    fave = favorites.objects.filter(id_user_id = id)
    # print(fave)
    
    # if request.user.is_authenticated == False:
    #     return redirect('/')
    films_list = films.objects.raw('SELECT database_films.id as id,database_films.title, database_films.path, database_films.rating FROM database_films WHERE database_films.id = %s', [film_id,])
    genre = []
    # print(len(films_list))
    if len(films_list) ==0:
        context={
            'title': 'Ошибка',
            'text' : 'Такого фильма не существует в списке',

        }
        return render(request,'films/fail.html', context)
    film_list_x = []
    for elem in films_list:
        e =elem.__dict__
        film_list_x.append((e['id'],e['title'], e['path'], e['rating']))
    id = film_list_x[0][0]
    title = film_list_x[0][1]
    path = film_list_x[0][2]
    rate = film_list_x[0][3]
    fl = 0
    if request.method == 'GET':
        h = history(date = datetime.datetime.now(),title = title, id_film_id = id, id_user_id = id_u)
        h.save()
    for elem in fave:
        print(elem.__dict__)
        if elem.__dict__['id_film_id'] == id:
            fl = 1
    
    # print(request.__dict__)
    # # print(request.user, request.user.is_authenticated)
    # print(request.user.__dict__['_wrapped'] == 'GOGa')
    
    context = {
        'id': id, 
        'title':title,
        'path': '../../media/'+path,
        'rating': rate
        
        
        
    }
    if request.method == 'POST':
        dict_of_get = request.__dict__
        dict_of_post = dict(request._post)
        print(dict_of_post)
        form = Commentform(request.POST)
        # print(request.user, user.objects.filter(username = ))
        # c = comments.objects.create(text = dict_of_post['com'][0], )
        context['form']= form
        k = list(request._post.keys())

        # x = request._post['text_com']
        print(k,'text_com' in k)
        if 'tofavourite' in k:
            if fl == 0:
                f = favorites(title = title, id_film_id = id, id_user_id = id_u)
                f.save()
        
        if 'text_com' in k:
            # print(request._post, str(request.user))
            x = user.objects.filter(username = str(request.user))
            id = 1
            for elem in x:
                e =elem.__dict__
                id =e['id']
            s = request._post['text_com']
            print(request._post['text_com'])
            if 'id_com' in k:
                x = str(request._post['id_com'])
                print(str(request._post['id_com']))
                if x!= '':
                    s += ' Ответный комментарий на '+ str(request._post['id_com'])
                

            com = comments(text = s, id_author_id = id)
            
            # print(com)
            com.save()
            if 'id_com' in k:
                x = str(request._post['id_com'])
                if x != '':
                    con = prev_next_comm(id_child_id = com.id, id_parent_id = request._post['id_com'])
                    con.save()
            rat = rating(id_author_id = id, id_of_art_film = context['id'], id_content_id = com.id, rating = request._post['ra'], context = 'film')
            rat.save()
    id = film_list_x[0][0]
    rates_list = rating.objects.raw('SELECT 1 as id, id_content_id, rating, text from database_rating INNER JOIN database_comments on database_rating.id_content_id = database_comments.id WHERE context=%s AND id_of_art_film = %s',['film', id])
    rate_l =[]
    
    for elem in rates_list:
        e =elem.__dict__
        rate_l.append((e['id_content_id'], e['text'], e['rating']))
            

            
    print(rate_l)        
    context['comment_list'] = rate_l
    
    return render(request,'films/film.html', context)


