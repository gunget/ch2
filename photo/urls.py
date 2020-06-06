from django.conf.urls import url
from photo.views import *

app_name = 'photo'

urlpatterns =[
    # ex. '/'
    url(r'^$', AlbumLV.as_view(), name='index'),
    # ex. '/album/'. '/'과 똑같음
    url(r'^album/$', AlbumLV.as_view(), name='album_list'),
    # ex. '/album/99/'
    url(r'^album/(?P<pk>\d+)/$', AlbumDV.as_view(), name='album_detail'),
    # ex. '/photo/99/'
    url(r'^photo/(?P<pk>\d+)/$', PhotoDV.as_view(), name='photo_list'),
]