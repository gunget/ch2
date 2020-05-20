from django.conf.urls import url
from bookmark.views import BookmarkDV, BookmarkLV

# app_name = 'bookmark' #루트url에서 path함수가 아닌 url함수로 include해서 필요하지 않은 듯.
                        #아니면, 루트 url에서 namespace(반복되는 url부분)을 지정해서 필요치 않은 듯.
urlpatterns = [
    url(r'^$', BookmarkLV.as_view(), name='index'), #/bookmark/
                                                    #이 패턴의 이름은 bookmark:index가 됨
    url(r'(^?P<pk>\+d)/$', BookmarkDV.as_view(), name='detail'), #ex. /bookmark/1/
                                                    #이 패턴의 이름은 bookmark:detail이 됨
]
