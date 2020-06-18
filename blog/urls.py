from django.conf.urls import url
from django.urls import path
from blog.views import *

app_name = 'blog' #루트 url에서 namespace로 지정한 이름. 꼭 써줘야 defualt url이 됨

urlpatterns =[
    url(r'^$', PostLV.as_view(), name='index'),
    # /. blog/에서 blog는 namespace에서 지정한 부분
    url(r'^post/$', PostLV.as_view(), name='post_list'),
    #위와 동일. 패턴명만 다름
    url(r'^post/(?P<slug>[-\w]+)/$', PostDV.as_view(), name='post_detail'),
    #\w는 문자+숫자. '-'가들어간 문자숫자가 하나이상. ex. post/django-example/
    url(r'^archive/$', PostAV.as_view(), name='post_archive'),
    # ex. archive/
    url(r'^(?P<year>\d{4})/$', PostYAV.as_view(), name='post_year_archive'),
    # ex. 2012/
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', PostMAV.as_view(), name='post_month_archive'),
    # ex. 2012/nov/
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/$', PostDAV.as_view(),
        name='post_day_archive'),
    # ex. 2012/nov/10/
    url(r'^today/$', PostTAV.as_view(), name='post_today_archive'),
    # ex. today/
    url(r'^tag/$', TagTV.as_view(), name='tag_cloud'),
    # ex. tag/
    url(r'^tag/(?P<tag>[^/]+(?u))/$', PostTOL.as_view(), name='tagged_object_list'),
    # ex. tag/tagname/
    #[^/]+ : /이외의 문자가 하나이상 있다. (?u)앞의 구문을 유니코드로 인식해라(한글이 와도 인식되도록)
    url(r'^search/$', SearchFormView.as_view(), name='search'),
    #폼을 보여주고 폼에있는 데이터를 처리하기 위해 FormView를 상속받아 정의
    #blog/search/
    path('add/', views.PostCreateView.as_view(), name='add'),  # /Post/add/
    path('change/', views.PostChangeLV.as_view(), name='change'),  # /Post/change/
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='update'),  # /Post/99/update/
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),  # /Post/99/delete/
    # url()은 re_url로 대체. views.뷰클래스명.as_view()쓰는 패턴에 유의

]

