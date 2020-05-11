from django.contrib import admin
from bookmark.models import Bookmark
#bookmark폴더의 모델스파일에서 Bookmark라는 클래스를 가져와라

class BookmarkAdmin(admin.ModelAdmin):
    #admin싸이트에 Bookmark클래스가 어떤 모습으로 보여줄지 정의하는 클래스. 클래스를 상속받아 처리
    list_display = ('title', 'url')# 상속받은 class의 필수 변수. 자동으로 뜸

admin.site.register(Bookmark, BookmarkAdmin)#이걸 등록해야 admin사이트에서 내가 만든 DB를 볼수 있는듯
