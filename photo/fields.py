#썸네일 기능 제공하는 다양한 라이브러리 존재(sorl-thumbnail등)
#여기선 중고급 개발자를 위해 커스텀라이브러리를 직접 개발함

from django.db.models.fields.files import ImageField, ImageFieldFile
#커스텀 필드 작성을 위해 비슷한 역할을 하는 필드를 상속받음 -> ImageField
#이미지를 파일시스템에 쓰고 지우기 위해 ImageFieldFile도 상속
from PIL import Image
#이미지처리 라이브러리인 PIL(PIL의 python3.0 fork버전이 pillow) 임포트
import os


def _add_thumb(s): #'/경로/파일명.확장자'가 인수로 넘어 옴. 파일명.thumb.jpg로 썸네일 이름 바꾸는 함수
    parts = s.split('.')
    #점으로 쪼개주면 [파일명, 확장자]가 될 것
    parts.insert(-1, 'thumb')
    #insert(a, x) a번째에 x를 집어넣어라. 이때의 -1은 뒤에서 부터 한칸 지나온 자리. 뒤에서 두번째 자리.
    #뒤에서 두번째에 thumb라는 글자를 넣어라 [파일명, thumb, 확장자]
    if parts[-1].lower() not in ['jpg', 'jpeg']:
        #a[-1]은 리스트상 제일 뒤의 아이템. 곧 확장자가 jpg나 jpeg가 아니면,
        parts[-1] = 'jpg' #jpg로 바꿔라
    # a[-1]과 a[:-1]은 지칭하는 대상이 다르다!
    return '.'.join(parts) #part의 대상들을 '.'으로 결합해라(문자는 가능) -> '파일명.thumb.jpg'

class ThumbnailImageFieldFile(ImageFieldFile):
    #이미지 처리 필드는 경로(path)와 url속성을 제공해야 함

    #원본파일의 경로인 path속성에 추가해, 썸네일의 경로인 thumb_path속성을 만들어 주는 함수
    def _get_thumb_path(self):
        return _add_thumb(self.path) #path는 장고.db.model.files 에서 제공하는 기능으로,
                            #경로명 + 파일명을 돌려주는 함수 인듯./경로/파일명.thumb.jpg가 리턴됨
    thumb_path = property(_get_thumb_path) #property중 get속성만 할당해 준 것임
    #propert()는 속성을 선언하는 문장. 이것의 간략화 방법이 @property로 데코레이터를 사용하는 것
    #property() 파이썬 기본 함수. 쉽게 인스턴스의 속성을 만들어주는 함수. get, set, del에 해당하는 함수를
    #만들고 인스턴스=property(g,s,d)설정을 해 놓으면, 인스턴스.g로 호출 했을때 get에 해당하는 함수가 실행됨
    #이게 없었다면 '인스턴스.함수()'로 호출해야 접근할 수 있음(여기선 x.thumb_path하면 getter함수가 실행됨).
    #실제로는 다른 언어의 private기능을 구현 할 때 사용. 사용자가 함부로 접근할 수 없는 변수
    #(private. __사용)를 함수로 선언하고, 이에 접근, 변경할 수 있도록 만들어주는 함수.
    #클래스 선언시 해당 함수 위에 @property를 하면 get함수로 변수처럼 이후에 접근해서 값을 사용할 수 있다.

    #원본파일의 url인 url속성에 추가해, 썸네일의 경로인 thumb_url속성을 만들어 주는 함수
    def _get_thumb_url(self):
        return _add_thumb(self.url) #url도 장고.db.model.files 에서 제공하는 기능으로,
                                      #경로명 중 파일명을 돌려주는 함수 인듯. 파일명.thumb.jpg가 리턴됨
    thumb_url = property(_get_thumb_url)

    def save(self, name, content, save=True): #이 클래스에서 파일을 저장하고 생성하는 메소드
        #save=True 단순히 초기값을 설정 한 것
        super(ThumbnailImageFieldFile, self).save(name, content, save) #부모 ImageFieldFile클래스의
        #save()메소드를 호출해서 원본 이미지 저장. 메소드 오버라이드가 일어나지 않도록 super()사용한 것.

        #클래스 상속 개념잡기
        #오버라이드는 부모클래스의 메소드와 자식메소드의 이름이 같을때 인스턴스에서 호출하면 자식메소드가 호출
        #되는 것을 의미(부모 클래스의 값이 덮혀쓰여짐)
        #클래스 상속시 메소드 오버라이드가 발생할 수 있는데, 오버라이드 없이 부모클래스의 메소드를 그대로 쓰고
        #싶을 때, super()를 사용한다. 다중상속(특히 a-b-d,a-c-d로 이어지는 마름모 상속)시 d호출시 a가
        #중복 호출될 수 있는데, python2.x에서는 상속 시 super(d, self)를 써주면 이를 막을 수 있다.
        #python3.x에서는 그냥 편하게 super()라고만 호출해줘도 중복호출 현상이 일어나지 않는다.
        img = Image.open(self.path) #필로우에서 이미지 불러오기

        img = Image.open(self.path)
        size = (128, 128)
        img.thumbnail(size)
        background = Image.new('RGB', size, (255, 255, 255))
        box = (int((size[0]-img.size[0])/2), int((size[1]-img.size[1])/2))
        background.paste(img, box)
        background.save(self.thumb_path, 'JPEG')

        # jpeg가 RGBA모드에는 적용되지 않아 코드에는 개정판 내용 변경 적용. 변경코드는 jiff도 적용가능.
        # size = (128, 128)
        # img.thumbnail(size, Image.ANTIALIAS) #이미지를 썸네일로 만들어라
        # #Image.thumbnail(size, resize_filter). antialias는 고해상도를 저해상도에서 표현할때
        # #이미지 깨짐 현상을 완화시키는 필터(손으로 문지른 효과)
        # background = Image.new('RGBA', size, (255,255,255,0))
        # #이미지와 동일한 크기, 색상은 흰색, 완전 불투명한 배경이미지를 새로 만듦
        # #RGBA라는 색상지정표를 사용하는데 (255,255,255)가 흰색, (0)이 불투명을 의미
        # background.paste(img, (int((size[0]-img.size[0])/2), int((size[1]-img.size[1])/2)))
        # #백그라운드 위에 이미지를 붙여라. 가로세로 크기 규정.
        # background.save(self.thumb_path, 'JPEG') #pillow의 save 규칙.
        # #위에서 property를 활용해 get함수를 지정했던 thumb_path가 x.thumb_path형식으로 사용됨

    def delete(self, save=True): #save=True역시 초기값을 설정한 것. delete시 원본 이미지뿐 아니라
                                 #썸네일 이미지까지 지워라 라는 명령
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super(ThumbnailImageFieldFile, self).delete(save)#delete(true)한 것

class ThumbnailImageField(ImageField): #장고 모델 정의에 사용하는 클래스
    attr_class = ThumbnailImageFieldFile #새로운 FileField클래스를 정의할 때는 그에 상응하는
    #file처리 클래스를 attr_class에 지정 해줘야 함

    def __init__(self, thumb_width=128, thumb_height=128, *args, **kwargs):
        #모델 정의 시, 썸네일 폭/너비 를 지정 할 수 있음. default=(128,128) px
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super(ThumbnailImageField, self).__init__(*args, **kwargs)