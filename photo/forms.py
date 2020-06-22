#폼셋이란 동일한 폼 여러개로 구성된 폼을 지칭. 또 인라인 폼셋이란 메인 폼에 딸려있는 하위 폼셋을 지칭
#테이블의 관계가 1:N일 경우, N테이블의 레코드 여러개를 동시에 입력받기 위한 용도로 인라인폼셋 사용.

from photo.models import Album, Photo
from django.forms.models import inlineformset_factory#인라인 폼셋을 만들어주는 메소드

PhotoInlineFormSet = inlineformset_factory(Album, Photo,
                    fields=['image', 'title', 'description'], extra=2)
#1:N에서 Album이 1, Photo가 N임을 지정. 폼셋에 사용할 필드를 지정하고, 빈폼 개수는 2개로 지정
