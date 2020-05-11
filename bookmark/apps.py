from django.apps import AppConfig


class BookmarkConfig(AppConfig): #앱에대한 메타정보를 저장하기 위한 클래스. start app하면 자동으로 생성
                                 # AppConfig상속받아 기록
    name = 'bookmark' #name은 필수속성. 그외 lable, path등 설정할 수 있음
