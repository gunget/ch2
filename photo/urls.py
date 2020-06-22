from django.conf.urls import url
from django.urls import path
from photo.views import *
from . import views

app_name = 'photo'

urlpatterns =[
    # ex. '/'
    url(r'^$', AlbumLV.as_view(), name='index'),
    # ex. '/album/'. '/'과 똑같음
    url(r'^album/$', AlbumLV.as_view(), name='album_list'),
    # ex. '/album/99/'
    url(r'^album/(?P<pk>\d+)/$', AlbumDV.as_view(), name='album_detail'),
    # ex. '/photo/99/'
    url(r'^photo/(?P<pk>\d+)/$', PhotoDV.as_view(), name='photo_detail'),

    path('album/add/', views.AlbumPhotoCV.as_view(), name='album_add'),
    #앨범과 포토를 한번에 처리하는 인라인 모델 폼을 처리하는 뷰. 생성용도.
    path('album/change/', views.AlbumChangeLV.as_view(), name='album_change'),
    #바꿀 수 있는 리스트를 단순 표시해주는 뷰
    path('album/<int:pk>/update/', views.AlbumPhotoUV.as_view(), name='album_update'),
    #앨범과 포토를 한번에 처리하는 인라인 모델 폼을 처리하는 뷰. 변경 용도.
    path('album/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album_delete'),

    path('photo/add/', views.PhotoCreateView.as_view(), name='photo_add'),
    #앨범과 포토를 한번에 처리하는 인라인 모델 폼을 처리하는 뷰
    path('photo/change/', views.PhotoChangeLV.as_view(), name='photo_change'),
    path('photo/<int:pk>/update/', views.PhotoUpdateView.as_view(), name='photo_update'),
    path('photo/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo_delete'),

]