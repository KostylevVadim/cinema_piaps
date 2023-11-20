from django.shortcuts import render
from django.contrib.auth import logout
from .forms import UserLoginForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, UpdateUserForm, UpdateProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth, messages
from django.core.paginator import Paginator

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

def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
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
        'form': form
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
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/")
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')

    return render(request, 'template/profile.html', {'user_form': user_form})


@login_required(login_url="/")
def favourite_films(request):
    if request.method == 'DELETE':
        films.objects.raw('''DELETE FROM favourite WHERE film_id = %s AND user_id=%s''', request.film.id, request.user.id)
    
    film_list_tmp = films.objects.raw('''SELECT database_films.id as id,database_films.title, database_films.path, database_films.rating FROM database_films
                                      INNER JOIN favourites ON favourites.film_id=database_films.id  WHERE user_id=%s''', request.user.id)
    film_list = []
    for elem in film_list_tmp:
        e =elem.__dict__

        film_list.append((e['id'],e['title'], e['path'], e['rating']))

    paginator = Paginator(film_list, 3)
    print(paginator.count, ' ',paginator.num_pages)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title':'Кинотеатр',
        'films': film_list,
        'page_obj': page_obj
    }
    return render(request,'template/favourite_films.html', context)

@login_required(login_url="/")
def add_post(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            title = form.cleaned_data.get('title')
            date = date.today()
            author = request.user.__dict__['wrapped'].__dict__['username']
            body = form.cleaned_data.get('body')
            id = articles.objects.create(title=title, body=body, author=author, date=date)
            id.save()
            article.id = id
            article.save()
        else:
            form = SignupForm()
    return render(request, 'template/post.html', {'form': form})

