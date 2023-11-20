from django.shortcuts import render
from django.contrib.auth import logout
from .forms import UserLoginForm, UpdateUserForm, UploadForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from django.contrib.auth.models import User
# from django.core.mail import EmailMessage
# from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth, messages

from database.models import user, info, films, articles


def login_not_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


@login_not_required(login_url='/')
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    _next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        _user = auth.authenticate(username=username, password=password)
        login(request, _user)
        if _next:
            return redirect(_next)
        return redirect('/')
    context = {
        'form': form,
        'title': 'Вход'
    }
    return render(request, 'login.html', context)


@login_not_required(login_url='/')
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            _user = form.save(commit=False)
            _user.is_active = True
            surname = form.cleaned_data.get('surname')
            name = form.cleaned_data.get('name')
            patronimic = form.cleaned_data.get('patronimic')
            _info = info.objects.create(surname=surname, name=name, patronimic=patronimic)
            _info.save()
            _user.id_info = _info
            _user.save()
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form, 'title': 'Регистрация'})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url="/")
def profile(request, profile_id):
    user_form = UpdateUserForm()
    d_user = request.user.__dict__['_wrapped'].__dict__
    current_data = [d_user['username']]
    #Показывать данные пользователя
    if request.method == 'POST':
        k = list(request._post.keys())
        # print(k, 'change_data' in k)
        if 'change_data' in k:
            user_form = UpdateUserForm(request.POST, instance=request.user)
            # print(user_form.__dict__)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your profile is updated successfully')
            # return redirect(to='users-profile')

    return render(request, 'profile.html', {'form': user_form, 'title' : "Профиль", 'data': current_data})

@login_required
def history(request):
    film_list_tmp = films.objects.raw('''SELECT database_films.id as id,database_films.title, database_films.path, database_films.rating FROM database_films
                                      INNER JOIN database_history ON database_history.id_film_id=database_films.id  WHERE id_user_id=%s''', [request.user.id,])
    film_list = []
    # print('here3')
    # print(film_list_tmp.__dict__)
    for elem in film_list_tmp:
        print(elem)
        e =elem.__dict__

        film_list.append((e['id'],e['title'], e['path'], e['rating']))

    paginator = Paginator(film_list, 3)
    # print(paginator.count, ' ',paginator.num_pages)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title':'История просмотра',
        'films': film_list,
        'page_obj': page_obj
    }
    return render(request, 'history.html', context)


@login_required(login_url="/")
def favourite_films(request):
    # print('here')
    if request.method == 'DELETE':
        films.objects.raw('''DELETE FROM favourite WHERE film_id = %s AND user_id=%s''', request.film.id, request.user.id)
    # print('here2')
    film_list_tmp = films.objects.raw('''SELECT database_films.id as id,database_films.title, database_films.path, database_films.rating FROM database_films
                                      INNER JOIN database_favorites ON database_favorites.id_film_id=database_films.id  WHERE id_user_id=%s''', [request.user.id,])
    film_list = []
    # print('here3')
    # print(film_list_tmp.__dict__)
    for elem in film_list_tmp:
        print(elem)
        e =elem.__dict__

        film_list.append((e['id'],e['title'], e['path'], e['rating']))

    paginator = Paginator(film_list, 3)
    # print(paginator.count, ' ',paginator.num_pages)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title':'Избранные фильмы',
        'films': film_list,
        'page_obj': page_obj
    }
    return render(request,'favourite_films.html', context)

class Create_article(CreateView):
    model = articles
    form_class = UploadForm

from django.core.files.storage import FileSystemStorage

@login_required(login_url="/")
def add_post(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        # print(request.user.__dict__, form.__dict__['fields']['id_author'].__dict__)
        if form.is_valid(request.user.id):
            obj = form.save(commit=False)
            print(obj.__dict__)
            obj.__dict__['id_author_id'] = 3
            form.save()
            
    else:
        form = UploadForm()
    return render(request, 'post.html', {'form': form})