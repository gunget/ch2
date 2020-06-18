from django.conf.urls import url
from django.urls import path, re_path
#일반적인 패턴은 path, 복잡한 정규식을 써야할 땐 re_path를 사용
from bookmark.views import BookmarkDV, BookmarkLV

app_name = 'bookmark' #루트 url에서 namespace로 지정한 부분. 이 부분이 default url이 됨

urlpatterns = [
    url(r'^$', BookmarkLV.as_view(), name='index'), #/bookmark/
                                                    #이 패턴의 이름은 bookmark:index가 됨
    url(r'^(?P<pk>\d+)/$', BookmarkDV.as_view(), name='detail'), #ex. /bookmark/1/
                                                    #이 패턴의 이름은 bookmark:detail이 됨
    path('add/', views.BookmarkCreateView.as_view(), name='add'), #/bookmark/add/
    path('change/', views.BookmarkChangeLV.as_view(), name='change'), #/bookmark/change/
    path('<int:pk>/update/', views.BookmarkUpdateView.as_view(), name='update'), #/bookmark/99/update/
    path('<int:pk>/delete/', views.BookmarkDeleteView.as_view(), name='delete'), #/bookmark/99/delete/
    #url()은 re_url로 대체. views.뷰클래스명.as_view()쓰는 패턴에 유의
]
