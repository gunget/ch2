from django.conf.urls import url
from bookmark.views import BookmarkDV, BookmarkLV

app_name = 'bookmark' #루트 url에서 namespace로 지정한 부분. 이 부분이 default url이 됨

urlpatterns = [
    url(r'^$', BookmarkLV.as_view(), name='index'), #/bookmark/
                                                    #이 패턴의 이름은 bookmark:index가 됨
    url(r'^(?P<pk>\d+)/$', BookmarkDV.as_view(), name='detail'), #ex. /bookmark/1/
                                                    #이 패턴의 이름은 bookmark:detail이 됨
]
