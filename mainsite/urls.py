"""mainsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin #기본적으로 로딩. admin싸이트 접속용도
from django.urls import path #기본적으로 로딩. path를 통해 보통은 접근
from django.conf.urls import url #보통 프로젝트용 url과 앱용 url 두개가 있으나, 여기선 프로젝트용
                                 #하나로만 바로 conf할꺼라 필요

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

urlpatterns = [
    url(r'^admin/', admin.site.urls), #장고 conf파일의 url함수는 내부적으로 re모듈을 호출하는 듯.
                                      #url()의 첫번째 변수가 regex 즉 정규식임
                                      #여기서 바로 정규식을 사용함. ^ ~로 시작하는.

    #Class-based view for bookmark 앱
    url(r'^bookmark/$', BookmarkLV.as_view, name='index'),# xx$ xx로 끝나야함
    #원래는 view.view처리함수 형태가 되어야 하나, 장고의 제네릭(표준)뷰를 쓰기 위해 as_view 사용
    #name은 이 url패턴을 뭐라고 부를 것인가를 정의하는 것
    url(r'^bookmark/(?P<pk>\d+)/$', BookmarkDV.as_view, name='detail'),
    #bookmark/11~/형태의 url. ?p<>는 정규식 그룹명을 지정한 것. 뷰를 호출할 때 primary key가
    #변수로 같이 넘겨짐. views.detal(request, pk)처럼.
]
