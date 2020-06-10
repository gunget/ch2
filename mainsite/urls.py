# url()와 path()의 차이
# path가 개선된 버전으로 사용 문법이 url에 비해 간략화 됨
# url(r'^book/(?P<pk>/d+)/$', views.book_detail)이
# path(r'^book/<int:pk>/', views.book_detail)로 바뀌어 간단하게 표현할 수 있음

from django.contrib import admin #기본적으로 로딩. admin싸이트 접속용도
from django.urls import path #기본적으로 로딩. path를 통해 보통은 접근
from django.conf.urls import url, include #보통 프로젝트용 url과 앱용 url 두개가 있으나, 여기선 프로젝트용
                                 #하나로만 바로 conf할꺼라 필요

from django.conf.urls.static import static #정적파일을 처리하는 뷰를 호출하도록 그에맞는 url패턴 반환
from django.conf import settings #settings변수 호출. setting.py에서 정의한 객체들을 담고 있음

# from bookmark.views import BookmarkLV, BookmarkDV
#view에서 정의한 클래스뷰들을 불러와서 url로 링크시켜야 해당 요구가 들어왔을때 링크해 줌

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from mainsite.views import HomeView #대문싸이트를 만들기 위한 view
from mainsite.views import UserCreateView, UserCreateDoneTV

urlpatterns = [
    url(r'^admin/', admin.site.urls), #장고 conf파일의 url함수는 내부적으로 re모듈을 호출하는 듯.
                                      #url()의 첫번째 변수가 regex 즉 정규식임
                                      #여기서 바로 정규식을 사용함. ^ ~로 시작하는.

    #인증관련 처리 URL
    url(r'^accounts/', include('django.contrib.auth.urls')),
    #django.co~는 장고가 기본적으로 제공하는 인증관련 앱으로, url과 템플릿파일명이 지정되어 있다. 책236페이지 표 참조
    url(r'^accounts/register/$', UserCreateView.as_view, name='register'),  #계정 생성처리를 하는 url
    url(r'^accounts/register/done/$', UserCreateDoneTV.as_view, name='register_done'), #생성 완료를 보여주는 url

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^bookmark/', include('bookmark.urls', namespace='bookmark')), #include 함수도 import해야함
    #최근에 url()대신해 path()가 소개됨. 해당 url이 들어오면 bookmark앱의 urls파일로 가서 처리해라
    #차이는 url에서 id를 추출하는 방식이 간편해짐. url은 ?<~~>였는데 path는(<int:number>형식)으로 간단해짐
    url(r'^blog/', include('blog.urls', namespace='blog')), #include 함수도 import해야함
    url(r'^photo/', include('photo.urls', namespace='photo')),
    #url(r'^photo/', ListView.as_view(model=Album), name='album_list'),로 한번에 할 수도 있음

##bookmark를 단독으로 urlconf할때 썻던 코드
    # #Class-based view for bookmark 앱
    # url(r'^bookmark/$', BookmarkLV.as_view(), name='index'),# xx$ xx로 끝나야함
    # #원래는 view.view처리함수 형태가 되어야 하나, 장고의 제네릭(표준)뷰를 쓰기 위해 as_view 사용
    # #name은 이 url패턴을 뭐라고 부를 것인가를 정의하는 것
    # url(r'^bookmark/(?P<pk>\d+)/$', BookmarkDV.as_view(), name='detail'),
    # #bookmark/11~/형태의 url. ?p<>는 정규식 그룹명을 지정한 것. 뷰를 호출할 때 primary key가
    # #변수로 같이 넘겨짐. views.detal(request, pk)처럼.
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) #개발과정에서 미디어파일을 처리하기 위해 추가
#statc(css, js같은 정적인 파일들)파일을 처리하는 url_conf를 추가(왜 쓰는지는 루트폴더에 작성해놓은 '장고 정적서비스 개념잡기 참조'
#static(prefix, view=django.views.static.serve, **kwarg)가 원래 용법
#즉, setting.py에서 MEDIA_URL로 지정한 url('/static/')이 들어오면 django.views.static~~이란
#뷰가 처리하고, 인수로 MEDIA_ROOT(os.path.join(BASE_DIR, 'media'))를 넘겨줘라 라는 것
#view는 장고가 제공하는 view니까 따로 코딩하지 않는 듯.

# static()함수의 다른 설명
# 정적 파일에 접근할 URL 접두사(staticfiles)를 첫 번째 인자로 넣고 정적 파일이 위치한 경로를 document_root라는 키워드 인자로 전달하면,
# 이런 내용을 django.views.static.serve라는 뷰 함수가 사용합니다. 이 serve 함수는 서버에 위치한 파일을 읽어서(open(fullpath, 'rb'))
# 스트리밍 방식으로 응답(StreamingHttpResponse)합니다. 실제 파일 서빙을 하는 것입니다. 물론 성능은 웹 서버가 직접 서빙하는 것보다 떨어지므로
# 개발 단계에서만 쓰는 게 좋을텐데, django.conf.urls.static의 static 함수는 settings의 DEBUG가 True인 경우에만 이런 정적 파일 제공에
# 필요한 URL 패턴을 만듭니다. 간단히 말해서 DEBUG=True인 경우에만 static 함수는 우리가 원하고 기대하는 동작을 합니다.
