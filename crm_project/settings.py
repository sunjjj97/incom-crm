"""
Django settings for crm_project project.
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=lambda v: [s.strip() for s in v.split(',')])

# CSRF 신뢰할 수 있는 origin 설정 (Django 4.0+)
# 환경 변수에서 설정 가능: CSRF_TRUSTED_ORIGINS=https://web-production-8c65.up.railway.app,https://another-domain.com
CSRF_TRUSTED_ORIGINS = []
try:
    csrf_origins_env = config('CSRF_TRUSTED_ORIGINS', default='', cast=str)
    if csrf_origins_env:
        CSRF_TRUSTED_ORIGINS = [s.strip() for s in csrf_origins_env.split(',') if s.strip()]
except Exception:
    CSRF_TRUSTED_ORIGINS = []

# Railway 환경에서 자동으로 도메인 감지 (환경 변수가 없을 경우)
if not CSRF_TRUSTED_ORIGINS:
    try:
        # 1. Railway가 제공하는 환경 변수 확인
        railway_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
        if railway_domain:
            CSRF_TRUSTED_ORIGINS = [f'https://{railway_domain}']
        else:
            # 2. Railway 환경 확인 (DATABASE_URL이나 RAILWAY_ENVIRONMENT가 있으면 Railway 환경으로 간주)
            is_railway = os.environ.get('DATABASE_URL') or os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_STATIC_URL')
            
            if is_railway:
                # 3. ALLOWED_HOSTS에서 도메인 추출 시도
                allowed_hosts_str = os.environ.get('ALLOWED_HOSTS', '')
                if allowed_hosts_str and allowed_hosts_str != '*':
                    hosts = [h.strip() for h in allowed_hosts_str.split(',') if h.strip()]
                    CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in hosts if host and not host.startswith('*')]
                
                # 4. 여전히 설정되지 않았다면, Railway의 기본 도메인 패턴 사용
                # Railway 환경 변수에서 도메인 추출 시도
                if not CSRF_TRUSTED_ORIGINS:
                    # RAILWAY_STATIC_URL이나 다른 Railway 환경 변수에서 도메인 추출
                    railway_static = os.environ.get('RAILWAY_STATIC_URL', '')
                    if railway_static and 'railway.app' in railway_static:
                        # URL에서 도메인 추출
                        from urllib.parse import urlparse
                        parsed = urlparse(railway_static)
                        if parsed.netloc:
                            CSRF_TRUSTED_ORIGINS = [f'https://{parsed.netloc}']
                    
                    # 5. 마지막 대안: 현재 알려진 Railway 도메인 추가 (임시)
                    # Railway Variables에서 CSRF_TRUSTED_ORIGINS를 명시적으로 설정하는 것을 권장
                    if not CSRF_TRUSTED_ORIGINS:
                        # Railway 환경에서 기본 도메인 패턴
                        # 실제 도메인은 Railway Variables에서 설정하는 것이 좋습니다
                        print("Warning: CSRF_TRUSTED_ORIGINS가 설정되지 않았습니다. Railway Variables에서 CSRF_TRUSTED_ORIGINS를 설정하세요.")
    except Exception as e:
        print(f"CSRF_TRUSTED_ORIGINS 설정 중 오류: {e}")
        pass  # 오류가 발생해도 계속 진행


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # 숫자 포맷팅 (천단위 구분 기호)
    'crm_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crm_project.urls'

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

WSGI_APPLICATION = 'crm_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Database 설정
DATABASE_URL = os.environ.get('DATABASE_URL', None)

# Railway 서비스 간 변수 참조 처리 (${{Postgres.DATABASE_URL}} 형식)
if DATABASE_URL and DATABASE_URL.startswith('${{'):
    # Railway 변수 참조가 아직 치환되지 않은 경우, 환경 변수에서 직접 가져오기 시도
    print(f"⚠ Railway 변수 참조 감지: {DATABASE_URL}")
    print("Railway Variables에서 실제 DATABASE_URL 값을 설정하세요.")
    DATABASE_URL = None

# DATABASE_URL 값 정리 (앞뒤 공백 제거, None 체크)
if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.strip()
    if not DATABASE_URL or DATABASE_URL == 'None':
        DATABASE_URL = None

# Railway 환경 감지 (DATABASE_URL이 있으면 Railway/프로덕션 환경)
is_production = bool(DATABASE_URL)

if DATABASE_URL:
    try:
        # Railway, Render 등에서 제공하는 DATABASE_URL 사용 (PostgreSQL)
        print(f"PostgreSQL 데이터베이스 연결 시도 중...")
        print(f"DATABASE_URL 길이: {len(DATABASE_URL) if DATABASE_URL else 0}")
        
        # DATABASE_URL이 유효한 형식인지 먼저 확인
        if not DATABASE_URL or not isinstance(DATABASE_URL, str):
            raise ValueError(f"DATABASE_URL is empty or not a string: {type(DATABASE_URL)}")
        
        # 앞뒤 공백 제거
        DATABASE_URL = DATABASE_URL.strip()
        
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is empty after stripping whitespace")
        
        # 스킴(scheme) 검증
        if not DATABASE_URL.startswith(('postgresql://', 'postgres://')):
            raise ValueError(f"Invalid DATABASE_URL format. Must start with 'postgresql://' or 'postgres://', got: '{DATABASE_URL[:50]}...' (length: {len(DATABASE_URL)})")
        
        # '://'만 있는 경우 체크
        if DATABASE_URL.startswith('://'):
            raise ValueError(f"Invalid DATABASE_URL format. Missing scheme. Got: '{DATABASE_URL[:50]}...'")
        
        print(f"DATABASE_URL 형식 확인 완료 (처음 30자: {DATABASE_URL[:30]}...)")
        
        # 데이터베이스 연결 설정 (타임아웃 및 재시도 설정 포함)
        db_config = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
        # 연결 타임아웃 및 옵션 추가
        db_config['OPTIONS'] = {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000'  # 30초 쿼리 타임아웃
        }
        DATABASES = {
            'default': db_config
        }
        print(f"✓ PostgreSQL 데이터베이스 연결 성공: {DATABASES['default']['ENGINE']}")
        print(f"✓ 데이터베이스 호스트: {DATABASES['default'].get('HOST', 'N/A')}")
    except Exception as e:
        # DATABASE_URL 파싱 실패 시 오류 출력
        print(f"✗ DATABASE_URL 파싱 실패: {e}")
        print(f"DATABASE_URL 값 전체 (길이: {len(DATABASE_URL) if DATABASE_URL else 0}): {repr(DATABASE_URL)}")
        print("경고: 프로덕션 환경에서 DATABASE_URL 파싱 실패 시 애플리케이션이 시작되지 않습니다.")
        print("Railway Variables에서 DATABASE_URL을 확인하세요.")
        print("올바른 형식: postgresql://사용자명:비밀번호@호스트:포트/데이터베이스명")
        # 프로덕션 환경에서는 SQLite로 폴백하지 않고 오류 발생시키기
        raise Exception(f"DATABASE_URL 파싱 실패: {e}. Railway Variables에서 DATABASE_URL을 확인하세요. (현재 값: {repr(DATABASE_URL[:100])})")
else:
    # 로컬 개발 환경 (SQLite)
    print("로컬 개발 환경: SQLite 데이터베이스 사용")
    print("⚠ DATABASE_URL이 설정되지 않았습니다. 프로덕션 환경에서는 DATABASE_URL을 설정해야 합니다.")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login settings
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

