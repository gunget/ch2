from django.contrib import admin
from photo.models import Album, Photo

class PhotoInline(admin.StackedInline):
    #앨범과 포토는 1:N의 관계. 앨범을 보여줄 땐 앨범에 연결된 포토를 다 보여줄 수 있는데
    #이를 종방향으로 보여줄거면 StackedIn~, 횡방향으로 보여 줄거면 TabularIn~으로 설정
    model = Photo #추가로 보여줄 테이블은 포토테이블
    extra = 2 #이미 입력된 객체 외에 추가로 입력할 수 있는 객체 수 2개(admin사이트에서 입력하니까)

class AlbumAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    #앨범객체를 보여줄때 PhotoInline에서 정의한 내용도 같이 보여줘라
    list_display = ('name', 'description')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date')

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)

# Register your models here.
