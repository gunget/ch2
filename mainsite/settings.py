"""
Django settings for mainsite project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# __file__ 파일을 실행하면 해당 파일명이 들어오는 파일의 이름공간.
#os.path.abspath(__file__)현재 실행파일의 절대경로 표시. ~~/ch2/mainsite/setting.py
#os.path.dirname()은 해당위치의 디렉토리명만 얻어옴. 이를위해 마지막 '/'이후의 값은 떨굼.
# ~~/ch2/mainsite. 위에선 이것을 한번 더 써서 마지막 디렉토리가 한 단계 위로 올라오도록 함
# ~~/ch2. 결국 BASE_DIR = '~~/ch2'가 되는 것

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!_@)fh9#5-uh$b!u@&4ct856od%!7o36efa+^ujbsw1nae@q1x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition : 여기에 만든 앱을 등록해야 사용할 수 있음

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookmark.apps.BookmarkConfig',
    'blog.apps.BlogConfig',#북마크라는 폴더의 앱스파일 내에 북마크컨픽 클래스.
    'tagging.apps.TaggingConfig',#lib/site pakage/에 가보면 django-tagging이 설치되었는데
    #이를 프로젝트에 사용하려면 등록해야 함. 앱명이 tagging이고 패키지의 apps.py에 들어가서 앱에대한 정보를 보면
    #TaggingConfig라는 클래스로 만들어져 있으므로 이를 등록해야 함
    'disqus', #댓글기능을 제공하는 웹서비스. site pakage-disqus로 가보면 apps.py가 정의 되지 않음. 따라서
    # #그냥 disqus라고 등록하면 됨
    'django.contrib.sites', #disqus는 이 패키지를 사용하는 모든 사이트를 구별해야하므로, 장고에서는 각
    #사이트에 구별자(ID)를 제공해야 하는데, site패키지가 그 역할을 함. 이 패키지는 테이블이 존재하므로 migration
    #해야함
    'photo.apps.PhotoConfig',
]

# DISQUS_API_KEY = 'yhZgJVNydzBkddkx2pwaOv1cC48zwlnHfuC45eo4djDD8MBEkkoGaVjIJ1c4xJ2c'
DISQUS_WEBSITE_SHORTNAME = 'djangoprg' #DISQUS-Admin-setting-general에서 가져온 값
SITE_ID = 1 #django.contrib.sites에서 사이트를 구별하기 위해 지정한 값. 모두 달라야 함


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mainsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], #초기설정1
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mainsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'ko-kr' #admin사이트 메뉴 한글 표시 시

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] #초기설정2 ~~/ch2/static

#파일 업로드 기능 개발할때 필요한 미디어 설정. 10장부터 사용예정
MEDIA_URL = '/media/'
MEDIA_ROOT = [os.path.join(BASE_DIR, 'media')] #초기설정3 ~~/ch2/media
