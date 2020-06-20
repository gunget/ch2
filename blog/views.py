from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from blog.models import Post
from tagging.models import Tag, TaggedItem
from tagging.views import TaggedObjectList

from django.views.generic.edit import FormView
from blog.forms import PostSearchForm #검색 form으로 사용할 Post~~클래스를 임포트. 직접 만든 것
from django.db.models import Q  #검색에 필요한 기능은 장고의 Q클래스를 임포트
from django.shortcuts import render #단축함수 render

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
#reverse()함수를 쓰려면 url.py가 메모리에 로딩되어야 하는데, view처리 단계에서 로딩되지 않을수도
#있으므로 reverse_lazy함수를 썼다고 함
from django.contrib.auth.mixins import LoginRequiredMixin
# from mainsite.views import LoginRequiredMixin. 저자는 자기가 LoginRequiredMixin을
#직접 정의했지만, 이후에 장고에서 직접 만든 듯. 원리는 마찬가지로 Login~~를 상속한 view가 있다면
#해당 클래스의 as_view함수에 login_required를 적용시켜 반환시킴
from mainsite.views import OwnerOnlyMixin

''' 함수형 뷰였을 경우에는 첫째, DB에서 쿼리를 통해 데이터를 가져와 객체1을 만들고(Queryset)
둘째, 딕셔너리 형태로 템플릿에서 사용하게 컨텍스트 변수(변수명:객체1 형식)를 만들고
셋째, render함수로 지정된 템플릿파일에 컨텍스트 변수를 적용시킨 HTML텍스트를 만들어서
넷째, 역시 render함수가 이를 HttpResponse객체에 담아 반환하는 작업을 한다. 

제네릭 뷰가 이같은 과정을 축약해 위처럼 한줄의 코드로 만들어 버린것. 곧 자동으로 컨텍스트 변수는
object_list로, 템플릿파일은 모델명소문자_list.html(post_list.html)로 지정된다.
'''
'''
같은 맥락에서, generic view를 상속받을 때는 뷰처리 결과, 첫째 어떤 컨텍스트 변수가 템플릿으로 넘겨지는지와
둘째 어떤 이름의 템플릿으로 변수를 넘겨주는지를 파악해야 한다. 그래야 템플릿을 작성할 때 올바른 변수들을 활용할 수 있다.
이는 장고 라이브러리에서 찾아 볼 수밖에 없다(from의 항목의 라이브러리를 검색하면 클래스들은 세부설명에 있다).  
'''

#template View
class TagTV(TemplateView):
    template_name = 'tagging/tagging_cloud.html'
#템플릿뷰는 테이블 처리없이 단순히 템플릿 렌더링만 하는 뷰

#List View
class PostLV(ListView): #상속을 받았기에 변수들이 고정되어 있음.
    model = Post #테이블은 Post란 클래스명으로 지정되었다.
    template_name = 'blog/post_all.html' #컨텍스트 변수를 적용시킬 지정 html
                                         #지정안하면 blog/post_list.html로 자동 설정됨
                                         #앞의 blog는 템플릿안에 blog폴더를 하나더 만들어준 것 의미
    context_object_name = 'posts' #템플릿파일로 넘겨주는 객체 리스트에 대한 컨텍스트 변수명을 post로 지정
                                  #디폴트 변수명인 'object_list'역시 사용 가능
    paginate_by = '2' #페이지 지정 옵션. 한 페이지에 보여주는 객체리스트의 숫자는 2개
                      #이렇게 설정 하는 것만으로 장고의 페이징 기능 쓸 수 있음. 하단에 페이지 이동버튼 사용가능
                      #page_obj라는 페이지 객체가 넘겨지는 듯

class PostTOL(TaggedObjectList):
    model = Post
    template_name = 'tagging/tagging_post_list.html'
#tagged object List는 listview를 상속받는 제네릭뷰로 모델과 태그가 주어지면 태그가 달린 모델의 객체리스트를 보여줌
#list view를 상속받았으므로 object_list를 컨텍스트 변수로 템플릿에 넘겨 줌

#Detail View
class PostDV(DetailView): #테이블에서 특정 개체를 가져와 그 상세정보를 출력
    model = Post #객체를 조회하기 위한 키는 slug로 urlconf에서 자동츠로 추출해 넘겨줌(조회키 사용 안함)

#Archive View
class PostAV(ArchiveIndexView): #테이블에서 객체 리스트를 가져와 날짜 필드를 기준으로 최신객체를 먼저 출력
    model = Post
    date_field = 'modify_date' #modify_date컬럼을 날짜 필드로 사용 = 즉 최근에 수정된게 가장 먼저 나옴
                               #modify_date는 컬럼을 지정했던 변수명. 모델에서 지정한 별칭을 쓰지 않음
#장고 라이브러리를 찾아보면 ArchiveIndexView에서 넘겨주는 컨텍스트 변수와 적용시킬 html의 명칭이 나온다.
#A~I~V에서는 data_list와 object_list를 넘겨준다. html은 post_archive.html이된다.

class PostYAV(YearArchiveView): #테이블에서 날짜 필드의 연도를 기준으로 객체리스트를 가져와, 그 객체들이 속한
                                #리스트를 출력. 날짜필드의 연도 파라미터는 urlconf에서 넘겨줌
                                # => 즉 해당 년도에 작성한 리스트들을 표시함
    model = Post
    date_field = 'modify_date' #modify_date컬럼을 날짜 필드로 사용
                               #modify_date는 컬럼을 지정했던 변수명. 모델에서 지정한 별칭을 쓰지 않음
    make_object_list = True #해당년도의 객체 리스트를 만들어서 템플릿에 넘겨줌. 템플릿에서는 object_list
                            #컨텍스트 변수를 활용 가능. default는 false

class PostMAV(MonthArchiveView): #테이블에서 날짜 필드의 연월를 기준으로 객체리스트를 가져와, 그 객체들이 속한
                                # 리스트를 출력. 날짜필드의 연월 파라미터는 urlconf에서 넘겨줌
                                # => 즉 해당 년월에 작성한 리스트들을 표시함
    model = Post
    date_field = 'modify_date' #modify_date컬럼을 날짜 필드로 사용

class PostDAV(DayArchiveView): #테이블에서 날짜 필드의 연월일 기준으로 객체리스트를 가져와, 그 객체들이 속한
                                #리스트를 출력. 날짜필드의 연월일 파라미터는 urlconf에서 넘겨줌
                                # => 즉 해당 년월일에 작성한 리스트들을 표시함
    model = Post
    date_field = 'modify_date' #modify_date컬럼을 날짜 필드로 사용

class PostTAV(TodayArchiveView): #오늘에 해당하는 아카이브를 불러줌. 오늘 이란 점만 빼고 dayArchive와 동일
    model = Post
    date_field = 'modify_date' #modify_date컬럼을 날짜 필드로 사용

#FormView

class SearchFormView(FormView): #search/ url을 처리할 view. formView 제네릭뷰를 상속받음
    #일반적으론 폼을 보여주는 뷰, 데이터를 처리하는 뷰를 하나로 묶어서 처리하는데, 이때 입력된 데이터가
    #유효한지를 검사해 맞다면 적절한 처리후 특정 url로 리다이렉트 시킨다.

    #위와같은 form처리 절차를 FormView로 간략화한 듯.
    #formView는 get요청인 경우 form을 화면에 보여주고 입력을 기다림
    #사용자가 입력 후 제출하면, 데이터의 유효성을 검사한 후,
    #데이터가 유효하면 form_valid()함수를 실행 후 적절한 url로 re-direct 시킴
    form_class = PostSearchForm #form으로 사용할 클래스는 이거다라고 지정
    template_name = 'blog/post_search.html'
    #검색 결과를 보여줄 템플릿

    def form_valid(self, form): #post요청으로 들어온 데이터에 유효성 검사후 이상이 없으면, 이를 실행
        schWord = '%s' % self.request.POST['search_word']
        #'search_word'는 post요청으로 넘어온 검색어 변수값(필드 id이기도).
        post_list = Post.objects.filter(Q(title__icontains=schWord) |
        Q(description__icontains=schWord) | Q(content__icontains=schWord)).distinct()
        # Q()객체는 and or같은 복잡한 조건의 검색을 해야할 때 사용하는 q객체를 만드는 함수
        # __icontains등은 filter()함수의 세부 조건.
        # 대소문자를 가리지 않고(icontains. 필터의 변수) schWord가 타이틀, 설명, 본문에 있는 지 검색해,
        # 중복된 건 빼고(distinct()) 리스트로 만들어라.

        context = {} #템플릿에 넘겨줄 콘텍스트 변수를 만든다
        context['form'] = form
        #PostSearchForm객체를 컨텍스트 변수 중 키워드 'form'에 지정
        context['search_term'] = schWord
        #검색 단어를를 컨텍스트 변수 중 키워드 'search_term'에 지정
        context['object_list'] = post_list
        #검색 결과를 컨텍스트 변수 중 키워드 'object_list'에 지정

        return render(self.request, self.template_name, context) #no re-direction
        #render는 템플릿파일과 컨텍스트 변수를 처리해 최종적으로 Httprespose객체를 반환함
        #form_vaild()함수는 보통 리다이렉트 처리를 위해 httpResposeRedirect객체를 반환하는데, 즉
        #마지막에 returen HttpResposeRedirect('url')이라고 쓰이는게 보통인데,
        #이 render함수에 의해 리다이렉트 처리가 되지 않는다.
        #한마디로 한페이지에 보여 주니까, 리다이렉트 처리를 하지 않는다 정도의 의미?

class PostCreatedView(LoginRequiredMixin, CreateView): #bookmarkCreateView와 내용 같음
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    initial = {'slug':'auto-filling-do-no-input'}
    #Post모델의 save()메소드에 의해 slug는 자동 생성됨. 그래서 입력하지 말라는 초기값을 넣어줌
    #fields = ['title', 'description', 'content', 'tag']. 아니면 이처럼 아예 빼버려도 됨
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form): #owner항목에 로그인 한 사람을 넣도록 form_valid재정의
        form.instance.owner = self.request.user
        return super(PostCreatedView, self).form_valid(form)

class PostChangeLV(LoginRequiredMixin, ListView):
    #북마크 테이블에서 현재 로그인 사용자에게 콘텐츠 변경이 허용된 객체만 보여주는 뷰
    #Log~~을 상속받으므로 login_required()데코레이터의 영향받음(로그인 한 사람 접근 가능)
    template_name = 'blog/post_change_list.html'

    def get_queryset(self):#현재 로그인된 사용자가 owner로 되어 있는 리스트만 뽑아내 리스트로 보여줌
        return Post.objects.filter(owner=self.request.user)

class PostUpdateView(OwnerOnlyMixin, UpdateView):
    #지정된 레코드 하나를 폼으로 보여주고, 수정된 내용의 유효성 검사 후, 에러없으면 테이블에 추가
    #Log~~을 상속받으므로 login_required()데코레이터의 영향받음(로그인 한 사람 접근 가능)
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    success_url = reverse_lazy('bookmark:index')#수정 완료 후 이동할 url

class PostDeleteView(OwnerOnlyMixin, DeleteView):
    #기존 레코드 중에서 지정된 레코드를 삭제할 것인지 여부를 묻는 싸이트를 보여준다.
    #Log~~을 상속받으므로 login_required()데코레이터의 영향받음(로그인 한 사람 접근 가능)
    model = Post
    success_url = reverse_lazy('blog:index')
