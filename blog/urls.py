from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path("", views.blog, name = 'articles'),
    path('<int:article_id>', views.article_id, name='article'),
    path('<int:article_id>/content', views.pdf_view),
    path("display", views.display)
]