from django.shortcuts import render

from django.views.generic import ListView, DetailView
from bookmark.models import Bookmark

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
#reverse()함수를 쓰려면 url.py가 메모리에 로딩되어야 하는데, view처리 단계에서 로딩되지 않을수도
#있으므로 reverse_lazy함수를 썼다고 함
from mainsite.views import LoginRequiredMixin
#@login_required()데코레이터 기능을 클래스에 적용 시 사용한다고 함

#----list view : 북마크 테이블의 레코드리스트를 보여주라는 처리방식
class BookmarkLV(ListView): #장고의 표준양식을 상속받아서 간단하게 리스트 표출
    model = Bookmark #상속받았을때 필수적으로 넣어야 함.
    ''' 함수형 뷰였을 경우에는 첫째, DB에서 쿼리를 통해 데이터를 가져와 객체1을 만들고
    둘째, 딕셔너리 형태로 템플릿에서 사용하게 컨텍스트 변수(변수명:객체1 형식)를 만들고
    셋째, render함수로 지정된 템플릿파일에 컨텍스트 변수를 적용시킨 HTML텍스트를 만들어서
    넷째, 역시 render함수가 이를 HttpResponse객체에 담아 반환하는 작업을 한다. 
    
    제네릭 뷰가 이같은 과정을 축약해 위처럼 한줄의 코드로 만들어 버린것. 곧 자동으로 컨텍스트 변수는
    object_list로, 템플릿파일은 모델명소문자_list.html(bookmark_list.html)로 지정된다.
    '''

#----Detail view : 북마크 테이블의 특정 레코드에 대한 상세정보를 보여주라는 처리방식
class BookmarkDV(DetailView): #장고의 표준양식을 상속받아서 간단하게 리스트 표출
    model = Bookmark
    ''' 마찬가지로 컨텍스트 변수는 object로 템플릿파일은 모델명소문자_detail.html로 자동 지정됨
    테이블에서 특정 객체를 가져오는 경우는(pk를 지정해서 호출할 경우) urlconf에서 넘어옴
    '''

class BookmarkCreateView(LoginRequiredMixin, CreateView):
    #LoginRe~~를 상속받는 클래스는 로그인된 경우에만 접근 가능. 로그인 되지 않은 상태에서 B~CreateView를
    #호출하면 로그인 페이지로 이동시킨다.
    #Createview를 상속받으면 아래 항목만 채워주면 적절한 폼을 보여주고, form에 입력된 내용에서 에러가 없으면
    #입력된 내용으로 테이블에 레코드를 생성한다.
    model = Bookmark #CreateView 기능을 적용할 테이블
    fields = ['title', 'url'] #CreateView의 기능에 따라 폼을 보여줄때, title과 url입력폼을 보여줌
    success_url = reverse_lazy('bookmark:index')#레코드 생성이 완료되었을때 이동할 url

    #데코레이터처럼 부모클래스의 메소드를 호출하기 전에 내용을 추가하고 싶을때, 이런식으로
    # 같은 이름으로 재정의 하는 듯. 결론은 부모클래스의 같은 메소드를 호출하게 됨.
    def form_valid(self, form): #form_vaild의 재정의. owner항목에 user의 이름을 넣기 위해.
        form.instance.owner = self.request.user
        #form의 owner필드에 로그인된 user객체를 할당
        return super(BookmarkCreateView, self).form_valid(form)
    #제출된 form의 유효성 검사를 마친 후 이상이 없으면 form_valid메소드를 호출 함(CreateView의 자동 기능)

class BookmarkChangeLV(LoginRequiredMixin, ListView):
    #북마크 테이블에서 현재 로그인 사용자에게 콘텐츠 변경이 허용된 객체만 보여주는 뷰
    #Log~~을 상속받으므로 login_required()데코레이터의 영향받음(로그인 한 사람 접근 가능)
    template_name = 'bookmark/bookmark_change_list.html'

    def get_queryset(self):#현재 로그인된 사용자가 owner로 되어 있는 리스트만 뽑아내 리스트로 보여줌
        return Bookmark.objects.filter(owner=self.request.user)

class BookmarkUpdateView(LoginRequiredMixin, UpdateView):
    #지정된 레코드 하나를 폼으로 보여주고, 수정된 내용의 유효성 검사 후, 에러없으면 테이블에 추가
    #Log~~을 상속받으므로 login_required()데코레이터의 영향받음(로그인 한 사람 접근 가능)
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')#수정 완료 후 이동할 url

class BookmarkDeleteView(LoginRequiredMixin, DeleteView):
    #기존 레코드 중에서 지정된 레코드를 삭제할 것인지 여부를 묻는 싸이트를 보여준다.
    #Log~~을 상속받으므로 login_required()데코레이터의 영향받음(로그인 한 사람 접근 가능)
    model = Bookmark
    success_url = reverse_lazy('bookmark:index')
