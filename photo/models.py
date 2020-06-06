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

from photo.fields import ThumbnailImageField
#원본이미지와 썸네일을 모두 저장할 수 있는 커스텀 필드(제공해주는 서드파티가 없으니 직접 제작).

@python_2_unicode_compatible
class Album(models.Model):#앨범과 포토의 관계는 1:N관계. 포토에서는 앨범의 Foreign키로 앨범에 대한 소속 구분
    name = models.CharField(max_length=50)
    description = models.CharField('One Line Description', max_length=100, blank=True)

    class Meta:#필드속성 외에 필요한 테이블의 파라미터를 정의하기 위해, 내부클래스 선언(이또한 상속받는 것)
        ordering = ['name'] #모델객체의 리스트 출력시 이름순(오름차순)으로 정렬
        #오름차순(ascending)은 순방향(일반적인 사용법 대로. 1-2-3, ㄱ-ㄴ-ㄷ, a-b-c). 오룸-일반(모두 ㅇ)
        #내림차순(descending)은 역방향(일반적인 사용법과 반대)

    def __str__(self):
        return self.name #어디서는 Album테이블의 객체를 호출하면, 그 객체의 name값을 표시하라.
                          #단, __str__을 적용해 문자형태로 알기쉽게 표기

    def get_absolute_url(self):
        return reverse('photo:album_detail', args=(self.id,))
        #photo앱의 album_detail이란 패턴명의 url을 추출해서 반환하는데 변수에는 id값을 넣어라.
        #ex. photo/album/1/

@python_2_unicode_compatible
class Photo(models.Model): #db에는 경로만 저장되고 파일을 media폴더에 저장된다.
    album = models.ForeignKey(Album, on_delete=models.CASCADE) #앨범테이블에 연결된 외래키.
    # 사진이 소속된 앨범객체를 가르킴. 연결된 앨범이 지워지면 photo도 지우라는 옵션(cascade) 추가(필수).
    # django2.0부터는 on_delete옵션을 추가해야함
    title = models.CharField(max_length=50)
    image = ThumbnailImageField(upload_to='photo/%Y/%m')
    #Thumb~~는 이미지, 썸네일 둘다 저장하는 커스텀 필드(장고가 아니라 서드파티에서 스스로 정의한 필드).
    #모델에서 가져오지 않았음에 주목!! upload_to로 저장할 위치 지정
    #세팅에 MEDIA_ROOT로 지정된 곳 하위에 ~/photo/2020/12처럼 폴더를 만들고 그곳에 사진 및 썸네일 저장
    description = models.TextField('Photo Description', blank=True)
    upload_date = models.DateTimeField('Upload Date', auto_now_add=True)
    #auto~~ 객체가 생성될 때 시간을 자동으로 저장. 즉 사진이 업로드 될 때 시간을 자동으로 저장

    class Meta:#필드속성 외에 필요한 테이블의 파라미터를 정의하기 위해, 내부클래스 선언(이또한 상속받는 것)
        ordering = ['title'] #모델객체의 리스트 출력시 이름기준 오름차순으로

    def __str__(self):
        return self.title #어디서는 Photo테이블의 객체를 호출하면, 그 객체의 title값을 표시하라.
                          #단, __str__을 적용해 문자형태로 알기쉽게 표기

    def get_absolute_url(self):
        return reverse('photo:photo_detail', args=(self.id,))
        #photo앱의 photo_detail이란 패턴명의 url을 추출해서 반환하는데 변수에는 id값을 넣어라.
        #ex. photo/photo/1/

# 모델을 잡고 나면 앱-admin파일로 가서 이 모델이 admin사이트에서 어떻게 보일지를 세팅해줘야 함
