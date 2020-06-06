from django.shortcuts import render
from django.views.generic import ListView, DetailView
from photo.models import Album, Photo

class AlbumLV(ListView):
    model = Album
    #template_name = 을 지정하지 않으면 default로 album_list.html이 됨
class AlbumDV(DetailView):
    model = Album

class PhotoDV(DetailView):
    model = Photo


# Create your views here.
