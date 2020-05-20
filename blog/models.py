from __future__ import unicode_literals #python 2.X 호완용
from six import python_2_unicode_compatible #python2.x대의 문자열 처리 방식을 3.x대로 바꿔주는 것
# from django.utils.encoding import python_2_unicode_compatible에서 장고 3.0.4부터 바뀜

from django.db import models
from django.urls import reverse
#from django.core.urlresolvers import reverse #django 2.0 버전에서는 삭제됨
#일반적을 url()은 외부에서 url주소가 주어지면 이를 특정뷰와 연결시켜주는 기능을 한다(path()도 같은 역할)
#(이때 이 패턴에 특정이름을 붙이기도). 반면에 reverse()는 주어진 view로부터 url을 뽑아내는 일을 한다.
#즉 뷰를 실행해 처리결과로 다른 뷰를 로드해야 할때(리다이렉션) reverse를 써서 url을 만든후 다시 연결하는 것.
#그런데 서로다른 앱에서 같은 패턴명을 사용하는 경우도 있다. 이를 구분하기 위해 reverse를 사용할때는
#'앱명:패턴명'을 넣어서 호출하면, 그것에 해당하는 url이 추출되어 장고에 제공된다.
#reverse('blog:post_detail', kwargs={'id':10}) = blog앱의 detail이란 패턴명의 url을 추출하는데
# id값은 10이다. = '/blog/10/'

@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField('TITLE', max_length=50) #TITLE은 컬럼 레이블
    slug = models.SlugField('SLUG', unique=True, allow_unicode=True, help_text=
                            'one word for title alias') #alias 별명, 별칭
    #slug는 페이지나 포스트를 설명하는 핵심단어의 집합. 웹개발에서는 제목에서 '조사, 전치사, 마침표'등을
    #뺀 후 띄어쓰기는 '_'로 넣어 만든다. 이걸로 페이지에 대한 url을 만들어 검색을 용이하게 한다(뜻이 표시되니까)
    #url대용이니까 unique해야하고 한글처리를 위해 allow_unicode도 해준다.
    description = models.CharField('DESCRIPTION', max_length=100, blank=True,
                                   help_text='simple description text')
    #빈칸으로 두어도 되도록 blank옵션을 추가
    content = models.TextField('CONTENT') #여러줄 입력가능
    creat_date = models.DateTimeField('Creat Date', auto_now_add=True)
    #날짜와 시간 기록하는 클래스. 생성 시 기록하도록 auto_now_add 활성화
    modify_date = models.DateTimeField('Modify Date', auto_now=True)
    #auto_now는 객체가 DB에 저장될 때 시각 자동기록. 즉 변경될 때 기록

    class Meta:#필드속성 외에 필요한 테이블의 파라미터를 정의하기 위해, 내부클래스 선언(이또한 상속받는 것)
        verbose_name = 'post' #테이블의 별칭. 변수명은 상속받는 것 활용(내맘데로 짓는게 아님)
        verbose_name_plural = 'posts' #테이블의 복수 별칭
        db_table = 'my_post' #DB에 저장되는 테이블의 이름(지정안하면 '앱명_모델클래스명'으로 자동 지정됨)
        ordering = ('-modify_date',) #모델객체의 리스트 출력시 변경일 기준, 내림차순으로 표시되도록

    def __str__(self):
        return self.title #어디서는 post테이블의 객체를 호출하면, 그 객체의 타이틀값을 표시하라.
                          #단, __str__을 적용해 문자형태로 알기쉽게 표기

    def get_absolute_url(self): #slug가 삽입된 전체 url을 표시하는 함수
        return reverse('blog:post_detail', args=(self.slug,))
        #blog앱의 post_detail이란 패턴명의 url을 추출해서 반환하는데 변수에는 slug값을 넣어라.
        #ex. blog/slug~

    def get_previous_post(self):
        return self.get_previous_by_modify_date()
        #수정된 날짜 기준으로 이전 포스트를 반환하라

    def get_next_post(self):
        return self.get_next_by_modify_date()
        #수정된 날짜 기준으로 다음 포스트를 반환하라


# 모델을 잡고 나면 앱-admin파일로 가서 이 모델이 admin사이트에서 어떻게 보일지를 세팅해줘야 함
