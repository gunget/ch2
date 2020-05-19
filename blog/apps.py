from django.apps import AppConfig


class BlogConfig(AppConfig): #앱에대한 메타정보를 저장하기 위한 클래스. start app하면 자동으로 생성
    name = 'blog' #이름은 필수
