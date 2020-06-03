from django import forms #폼을 클래스로 표현할 수 있도록 하는 기능을 forms에서 제공

class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='search word')
    #모델클래스를 정의하는 방법과 유사. 변수search_word는 필드에 대한 id로 각 필드를 구분하는 역할을 함