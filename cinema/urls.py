"""
URL configuration for cinema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from blog.views import IndexView
from django.contrib.auth.decorators import user_passes_test
from users import views as ex_views
login_forbidden =  user_passes_test(lambda u: u.is_anonymous, '/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name = 'index'),
    path('films/', include('films.urls', namespace='films')),
    path('login/', login_forbidden(ex_views.login_view), name='login'),
    path('logout/', ex_views.logout_view, name='logout'),
    path('signup/', login_forbidden(ex_views.signup), name='signup'),
    path("blog/", include("blog.urls",namespace='blog')),
    path('profile/<int:profile_id>', ex_views.profile, name = 'profile'),
    path('favourite/', ex_views.favourite_films, name = 'favourite'),
    path('history/', ex_views.history, name = 'history'),
    path('add_post/', ex_views.add_post, name = 'post')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    # print(urlpatterns)