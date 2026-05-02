# --- CONFIGURACIÓN DINÁMICA (PC vs AWS) ---

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',    # Para S3
    'productos',   # Tu app
]

# 2. El "pegamento" de Django (Esto es lo que faltaba)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crud_project.urls'

# 3. Configuración de HTML/Templates
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

WSGI_APPLICATION = 'crud_project.wsgi.application'
if DEBUG:
    # 1. Configuración para tu PC (Desarrollo)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    # Carpeta local para imágenes
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

else:
    # 2. Configuración para AWS (Producción)
    # Aquí conectamos a la base de datos RDS
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'cruddjango2025',
            'HOST': 'db-django.crekiisico9o.us-east-2.rds.amazonaws.com',
            'PORT': '5432',
        }
    }

    # Configuración de almacenamiento S3
    AWS_STORAGE_BUCKET_NAME = 'django-crud-assets' # Revisa si es 'assets'
    AWS_S3_REGION_NAME = 'us-east-2'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    # Esto le dice a Django que use S3 para TODO
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
    }

# --- Redirecciones de Login (Para ambos entornos) ---
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'lista_productos'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'