from django.conf.urls import url
from blog.views import *

urlpatterns =[
    url(r'^$', PostLV.as_view(), name='index'),
    # /. blog/에서 blog는 루트url에서 정의했으므로. url패턴의 이름은 blog:index가 됨
    url(r'^post/$', PostLV.as_view(), name='post_list'),
    #위와 동일. 패턴명만 다름
    url(r'^post/(?P<slug>[-\w]+/$', PostDV.as_view(), name='post_detail'),
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
]
