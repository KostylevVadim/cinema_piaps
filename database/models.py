from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
# Create your models here.

class films(models.Model):
    title = models.CharField(max_length=128, unique= True)
    path = models.CharField(max_length=128, unique = True)
    rating = models.DecimalField(max_digits=6, decimal_places= 2)
    

class info(models.Model):
    surname = models.CharField(max_length=128, null= True)
    name = models.CharField(max_length=128, null= True)
    patronimic = models.CharField(max_length= 128, null = True)

class user(AbstractUser):
    id_info = models.ForeignKey(to = info, on_delete= models.CASCADE, null= True)
    role = models.CharField(max_length=128)

class members(models.Model):
    id_info = models.ForeignKey(to = info, on_delete= models.CASCADE)
    job = models.CharField(max_length=128)
    image = models.ImageField(upload_to='member_photo')

class member_film():
    id_info = models.ForeignKey(to = members, on_delete= models.CASCADE)
    id_film = models.ForeignKey(to = films, on_delete= models.CASCADE)
    role = models.CharField(max_length=128)

class history(models.Model):
    id_user = models.ForeignKey(to = user, on_delete= models.CASCADE)
    id_film = models.ForeignKey(to = films, on_delete= models.CASCADE)
    date = models.DateField()
    # title = models.CharField(max_length=128)

class favorites(models.Model):
    id_user = models.ForeignKey(to = user, on_delete= models.CASCADE)
    id_film = models.ForeignKey(to = films, on_delete= models.CASCADE)
    # title = models.CharField(max_length=128)

class articles(models.Model):
    id_author = models.ForeignKey(to = user, on_delete= models.CASCADE)
    path = models.CharField(max_length= 128)
    date = models.DateField()
    title = models.CharField(max_length= 128)



class comments(models.Model):
    text = models.TextField()
    date = models.DateField()
    
class prev_next_comm(models.Model):
    id_parent = models.OneToOneField(to = comments, on_delete= models.CASCADE)
    id_child = models.ForeignKey(to = comments, on_delete= models.CASCADE, related_name='cild')

class genre(models.Model):
    name = models.CharField(max_length= 128)

class genre_film(models.Model):
    id_genre = models.ForeignKey(to = genre, on_delete= models.CASCADE)
    id_films = models.ForeignKey(to = films, on_delete= models.CASCADE)