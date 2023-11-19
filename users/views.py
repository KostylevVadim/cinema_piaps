from django.shortcuts import render
from django.contrib.auth import logout
from .forms import UserLoginForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from django.contrib.auth.models import User
# from django.core.mail import EmailMessage
# from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth, messages

from database.models import user, info


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
