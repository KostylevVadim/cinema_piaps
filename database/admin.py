from django.contrib import admin
from database.models import films, user, genre, info, articles
# Register your models here.

@admin.register(films)
class filmsadmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(user)
class useradmin(admin.ModelAdmin):
    model= user
    fields = ['username', 'role']

@admin.register(articles)
class articlessadmin(admin.ModelAdmin):
    list_display = ['title']
# @admin.register(info)
# class infoadmin(admin.ModelAdmin):
#     model = info
#     list_display = ['name', 'surname']
#     inlines = [useradmin,]

@admin.register(genre)
class classgenre(admin.ModelAdmin):
    list_display =['name']