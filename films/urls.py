
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from films.views import film, film_id
app_name = 'films'
urlpatterns = [
    path('', film, name = 'films'),
    path('film/<int:film_id>', film_id, name = 'film'),

]
