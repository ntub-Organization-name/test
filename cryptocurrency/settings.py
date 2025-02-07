"""
Django settings for cryptocurrency project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os
from pathlib import Path


env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f2_rtd0=h2-)c1oz1%n5olz5f*k8jc-9(3vy_*!xqpo(#qhj()'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'main',
    'django_celery_beat',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cryptocurrency.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


WSGI_APPLICATION = 'cryptocurrency.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 使用 MySQL 引擎，MariaDB 是與 MySQL 兼容的
        'NAME': 'cryptocurrency',  # 設定你的資料庫名稱
        'USER': os.getenv('DB_USER'),  # 設定你的資料庫用戶名
        'PASSWORD': os.getenv('DB_PASSWORD'),  # 設定你的資料庫密碼
        'HOST': 'localhost',  # 設定資料庫伺服器地址，'localhost' 或 MariaDB 的 IP 地址
        'PORT': '3306',  # 設定 MariaDB 的端口（預設端口為 3306）
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'zh-hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# 配置靜態文件的目錄
STATICFILES_DIRS = [
    BASE_DIR / "static", ] # 根目錄下的 static 資料夾

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'  # 未登入時跳轉到此頁面

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# settings.py

# 用於發送重設密碼郵件的 SMTP 配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # 使用 Gmail 的 SMTP 服務
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # 使用 TLS 加密
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # 使用你的 Gmail 地址（用來發送郵件）
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # 使用 Gmail 生成的應用程式專用密碼
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # 用來發送郵件的默認地址

#新增密碼強度(最小8碼)
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#         'OPTIONS': {
#             'min_length': 8,
#         },
#     },
# ]


'''
# Celery 設定
CELERY_BROKER_URL = 'amqp://localhost'  # RabbitMQ URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'rpc://'  # 可以選擇使用其他後端來存儲結果

from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'crawl-every-10-minutes': {
        'task': 'main.tasks.run_scraper',
        'schedule': crontab(minute='*/1'),  # 每 10 分鐘執行一次
    },
}
'''

from celery.schedules import crontab
from main.task import news_crawler
CELERY_BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Taipei'

CELERY_BEAT_SCHEDULE = {
    'news_crawler-every-1-hour': {
        'task': 'main.task.news_crawler',
        'schedule': 3600.0,
    },
    'fetch_history-every-5-minutes': {
        'task': 'main.task.fetch_history',  
        'schedule': 300.0, 
    },
}
