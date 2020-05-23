from django.contrib import admin
from blog.models import Post

class PostAdmin(admin.ModelAdmin): #post클래스(모델)가 admin site에서 어떻게 보일지 정의
    list_display = ('title', 'modify_date') #post객체를 보여줄때 타이틀과 수정일을 보여줘라. 장고의 지정 변수
                    #문자는 모델에서 선언한 변수명
    list_filter = ('modify_date',) #수정일 컬럼에 필터 사이드바가 나오도록 설정(,를 넣어줘야 튜플로 받아들여
                                   #makemigrations가 진행됨
    search_fields = ('title', 'content') # 검색창을 띄우는데, 검색은 '타이틀, 컨텐트'항목에서만 하도록.
    prepopulated_fields = {'slug':('title',)} #슬러그 항목은 타이틀 항목을 활용해 자동 채워지도록 설정
    #이 항목은 모델에서 설정해야할 것 같지만 admin에서 적용해야 함

admin.site.register(Post, PostAdmin) #post라는 모델과, 그 설정값을 admin사이트에 등록하라


#admin 세팅을 했으면, DB의 테이블 변동사항이 반영되도록 터미널에서 migration을 해줘야함.