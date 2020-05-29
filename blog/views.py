from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from blog.models import Post

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

