from __future__ import unicode_literals #python 2.X 호완용
from six import python_2_unicode_compatible #python2.x대의 문자열 처리 방식을 3.x대로 바꿔주는 것
# from django.utils.encoding import python_2_unicode_compatible에서 장고 3.0.4부터 바뀜

from django.db import models
#1새로운 DB를 만들려면 모델에 클래스를 만들고, 이를 admin사이트에 등록해야함
#2 manage.py파일을 이용해 makemigrations 실행, 변경사항 파일을 만들고, migrate로 이를 적용시킴
from django.contrib.auth.models import User

@python_2_unicode_compatible #함수를 인자로 갖는 또다른 함수(혹은 클래스)
#데코레이터. 파이썬이 함수를 또다른 함수의 '인자'로 쓸수 있다는 특징 활용(1st citizen class).
#@데코함수명, 바로 아래의 '다른 함수(클래스)'를 그대로 포장해서(wrap) 데코함수로 돌려주면, 데코함수에서는
#'다른 함수'앞(뒤)에 추가적인 작업을 한 후 전체 값을 돌려준다. 즉 다른 함수를 바꾸지 않고 추가적인 작업 수행
#즉 재활용하고픈 함수는 '다른 함수'이고, 추가하고픈 내용이 '데코 함수'이다.
class Bookmark(models.Model): #데이터베이스를 지칭하는 클래스. 장고의 Model클래스를 상속받아 간단히 처리.
    title = models.CharField(max_length=100, blank=True, null=True)#title이라는 칼럼만들기
    #blank=True이면 empty value 허용. null=true면 DB의 빈칸에 null이라고 입력.
    #옵션에 db_column값을 않넣으면 컬럼명에 변수명이 자동으로 들어감
    url = models.URLField('url', unique=True) #컬럼의 별칭 'url'(Field.verbose_name).
    # url은 단 하나만 있어야 하므로 unique를 True로
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True)
    #bookmark의 생성은 로그인 회원만 할 수 있도록 하기 위해, User테이블을 가져와 참조키롤 설정
    #기존에 만든 콘텐츠는 값이 null이므로 null을 True해놔야 함. 사용자가 지워지면 해당 bookmark가
    #따라서 지워지도록 on_delete항목을 CASCADE로 설정(필수). 따라지워지지 않으려면 PROTECT하면 됨

    def __str__(self): #admin사이트나 장고쉘에서 모델(테이블)의 개별 객체(row요소)를 표시할 때, '이것은
                   #어떤 객체다'라고 표시할 필요가 있는데(제목줄에 객체값을 쓰고, 아래 변경항목 나타낼 때)
                   #대표적으로 뭐라고 쓸 것인가를 결정. (__str__)을 적용, 이를 문자로 나타내 줌
        return self.title #어디서든 Bookmark테이블의 객체를 호출하면 그 객체의 타이틀값을 대표로 나타내라.
        #return '%s %s' %(self.title, self.url) #이면 객체를 불렀을 때 둘의 이름이 다 나올 것
