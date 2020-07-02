"""
WSGI config for mainsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 현재 장고 프로젝트 및 모든 어플리케이션에 대한 설정정보를 로딩하기 위해 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainsite.settings')

# 모든 어플리케이션 정보가 로딩되면, 별도로 설치된 웹서버는 이 application객체를 호출하여 사용자가 만든
# 어플리케이션들을 실행한다.
application = get_wsgi_application()
