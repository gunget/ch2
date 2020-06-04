from django.db.models.fields.files import ImageField, ImageFieldFile
#커스텀 필드 작성을 위해 비슷한 역할을 하는 필드를 상속받음 -> ImageField
#이미지를 파일시스템에 쓰고 지우기 위해 ImageFieldFile도 상속
from PIL import Image
#이미지처리 라이브러리인 PIL 임포트
import os

def _add_thumbs(s): #'파일명.확장자'가 인수로 넘어 옴. 파일명.thumb.jpg로 썸네일 이름 바꾸는 함수
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

class ThumbnailImageFile(ImageFieldFile):
    #이미지 처리 필드는 경로(path)와 url속성을 제공해야 함
    #원본파일의 경로를 활용해, 썸네일의 경로와 url을 만들어 주는 듯
    def _get_thumb_path(self):
        return _add_thumbs(self.path) #path는 장고.db.model.files 에서 제공하는 기능으로,
                                      #경로명 중 파일명을 돌려주는 함수 인듯. 파일명.thumb.jpg가 리턴됨
    thumb_path = property(_get_thumb_path) #property중 get속성만 할당해 준 것임
    #propert()는 속성을 선언하는 문장. 이것의 간략화 방법이 @property로 데코레이터를 사용하는 것
    #property() 파이썬 기본 함수. 쉽게 인스턴스의 속성을 만들어주는 함수. get, set, del에 해당하는 함수를
    #만들고 인스턴스=property(g,s,d)설정을 해 놓으면, 인스턴스.g로 호출 했을때 get에 해당하는 함수가 실행됨
    #이게 없었다면 '인스턴스.함수()'로 호출해야 접근할 수 있음.
    #실제로는 다른 언어의 private기능을 구현 할 때 사용. 사용자가 함부로 접근할 수 없는 변수
    #(private. __사용)를 함수로 선언하고, 이에 접근, 변경할 수 있도록 만들어주는 함수.
    #클래스 선언시 해당 함수 위에 @property를 하면 get함수로 변수처럼 이후에 접근해서 값을 사용할 수 있다.

    def _get_thumb_url(self):
        return _add_thumbs(self.url) #url도 장고.db.model.files 에서 제공하는 기능으로,
                                      #경로명 중 파일명을 돌려주는 함수 인듯. 파일명.thumb.jpg가 리턴됨
    thumb_url = property(_get_thumb_url)
