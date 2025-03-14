import os
from dotenv import load_dotenv
# Cargar las variables del archivo .env
load_dotenv()
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ji(y)%_w(&d5i@g7z+9nag$7(grgcno^bz(w(414+v$rv@yt@0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'  # Esto convierte el valor de 'DEBUG' a un booleano

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'LAPTOP-1DP06RFE',  # Agrega este valor
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',  # Asegúrate de que 'corsheaders' esté en la lista de aplicaciones
    'seguridad',
    'registros',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Este middleware debe estar al principio
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de CORS
CORS_ORIGIN_ALLOW_ALL = True  # Permite todos los orígenes (no recomendado en producción)
CORS_ALLOW_CREDENTIALS = True  # Permite el envío de credenciales (cookies, headers, etc.)

CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8000',  # Backend
    #'http://localhost:5173',  # Frontend Vue.js
    'http://localhost:5175',  # Frontend Vue.js (alternativo)
]

ROOT_URLCONF = 'apidivermind.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'apidivermind.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'apidivermind'),  # Asegúrate de que el nombre de la base de datos esté correcto
        'USER': os.getenv('DB_USER', 'apidivermind'),  # Usuario correcto
        'PASSWORD': os.getenv('DB_PASSWORD', 'apidivermind'),  # Contraseña correcta
        'HOST': os.getenv('DB_HOST', 'localhost'),  # Host, usualmente localhost
        'PORT': os.getenv('DB_PORT', '3306'),  # Puerto por defecto
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'