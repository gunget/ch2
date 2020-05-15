from django.shortcuts import render

from django.views.generic import ListView, DetailView
from bookmark.models import Bookmark

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
