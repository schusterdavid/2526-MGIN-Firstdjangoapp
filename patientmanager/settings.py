"""
Django settings for patientmanager.

Environment-driven settings file. Selects Azure SQL (mssql-django) when
AZURE_SQL_* env vars are present, falls back to Postgres if POSTGRES_HOST is set,
otherwise uses sqlite for local development.

This file intentionally avoids printing or storing secrets. The debug helper
only logs which backend branch was selected (Azure/Postgres/sqlite).
"""

from pathlib import Path
import os
import sys

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default')
DEBUG = os.environ.get('DEBUG', '1') == '1'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',') if os.environ.get('ALLOWED_HOSTS') else ['*']

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'patientmanagerapp',
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

ROOT_URLCONF = 'patientmanager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'patientmanager.wsgi.application'

# --- Database configuration (environment-driven) ---
AZURE_SQL_HOST = os.environ.get('AZURE_SQL_HOST')
AZURE_SQL_DATABASE = os.environ.get('AZURE_SQL_DATABASE')
AZURE_SQL_USERNAME = os.environ.get('AZURE_SQL_USERNAME')
AZURE_SQL_PASSWORD = os.environ.get('AZURE_SQL_PASSWORD')
AZURE_SQL_SERVERNAME = os.environ.get('AZURE_SQL_SERVERNAME')


def get_database_config():
    # Azure SQL via mssql-django
    if AZURE_SQL_HOST and AZURE_SQL_DATABASE and AZURE_SQL_USERNAME:
        user = AZURE_SQL_USERNAME
        if AZURE_SQL_SERVERNAME:
            user = f"{AZURE_SQL_USERNAME}@{AZURE_SQL_SERVERNAME}"

        return {
            'ENGINE': 'mssql',
            'NAME': AZURE_SQL_DATABASE,
            'USER': user,
            'PASSWORD': AZURE_SQL_PASSWORD,
            'HOST': AZURE_SQL_HOST,
            'PORT': os.environ.get('AZURE_SQL_PORT', ''),
            'OPTIONS': {
                'driver': os.environ.get('AZURE_ODBC_DRIVER', 'ODBC Driver 18 for SQL Server'),
            },
        }

    # Postgres fallback (if configured)
    if os.environ.get('POSTGRES_HOST'):
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('POSTGRES_HOST'),
            'PORT': os.environ.get('POSTGRES_PORT', ''),
        }

    # Default: sqlite
    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }


DATABASES = {'default': get_database_config()}

# Safe debug helper: prints which DB backend branch was chosen (no secrets)
if DEBUG and os.environ.get('PRINT_DB_SELECTION', '1') == '1':
    try:
        engine = DATABASES['default'].get('ENGINE', '')
        if 'mssql' in engine:
            selected = 'azure-sql (mssql)'
        elif 'postgresql' in engine:
            selected = 'postgresql'
        elif 'sqlite' in engine:
            selected = 'sqlite'
        else:
            selected = engine or 'unknown'
        print(f"[settings] selected database backend: {selected}")
    except Exception:
        # avoid crashing settings import
        print("[settings] could not determine selected database backend")

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"""
Django settings for patientmanager.

Single clean file: reads sensitive config from environment and supports
Azure SQL (mssql-django), Postgres, or sqlite fallback.
"""

from pathlib import Path
import os
"""
patientmanager settings (clean).

This file reads sensitive settings from environment variables. To use Azure SQL
set the AZURE_SQL_* variables (host, database, username, password, servername).
"""

from pathlib import Path
import os


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default')
DEBUG = os.environ.get('DEBUG', '1') == '1'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',') if os.environ.get('ALLOWED_HOSTS') else ['*']


# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'patientmanagerapp',
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

ROOT_URLCONF = 'patientmanager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'patientmanager.wsgi.application'


# Azure SQL env vars
AZURE_SQL_HOST = os.environ.get('AZURE_SQL_HOST')
AZURE_SQL_DATABASE = os.environ.get('AZURE_SQL_DATABASE')
AZURE_SQL_USERNAME = os.environ.get('AZURE_SQL_USERNAME')
AZURE_SQL_PASSWORD = os.environ.get('AZURE_SQL_PASSWORD')
AZURE_SQL_SERVERNAME = os.environ.get('AZURE_SQL_SERVERNAME')


def get_database_config():
    # Azure SQL via mssql-django
    if AZURE_SQL_HOST and AZURE_SQL_DATABASE and AZURE_SQL_USERNAME:
        """
        Django settings for patientmanager.

        Single, clean settings file that reads secrets from environment variables.
        Supports Azure SQL (mssql-django), Postgres, or sqlite fallback.
        Configure AZURE_SQL_* environment variables to use Azure SQL.
        """

        from pathlib import Path
        import os

        # Base directory
        BASE_DIR = Path(__file__).resolve().parent.parent

        # Security
        SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default')
        DEBUG = os.environ.get('DEBUG', '1') == '1'
        ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',') if os.environ.get('ALLOWED_HOSTS') else ['*']

        # Applications
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'patientmanagerapp',
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

        ROOT_URLCONF = 'patientmanager.urls'

        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ]

        WSGI_APPLICATION = 'patientmanager.wsgi.application'

        # --- Database configuration (environment-driven) ---
        # Azure SQL environment variables (set these to enable Azure SQL):
        AZURE_SQL_HOST = os.environ.get('AZURE_SQL_HOST')
        AZURE_SQL_DATABASE = os.environ.get('AZURE_SQL_DATABASE')
        AZURE_SQL_USERNAME = os.environ.get('AZURE_SQL_USERNAME')
        AZURE_SQL_PASSWORD = os.environ.get('AZURE_SQL_PASSWORD')
        AZURE_SQL_SERVERNAME = os.environ.get('AZURE_SQL_SERVERNAME')


        def get_database_config():
            """Return a DATABASE configuration dict based on environment variables.

            Priority:
              1) Azure SQL when AZURE_SQL_* variables are present
              2) Postgres when POSTGRES_HOST is present
              3) SQLite (local development) fallback
            """
            # Azure SQL via mssql-django
            if AZURE_SQL_HOST and AZURE_SQL_DATABASE and AZURE_SQL_USERNAME:
                # Some Azure setups require username in the form '<user>@<servername>'
                user = AZURE_SQL_USERNAME
                if AZURE_SQL_SERVERNAME:
                    user = f"{AZURE_SQL_USERNAME}@{AZURE_SQL_SERVERNAME}"

                return {
                    'ENGINE': 'mssql',
                    'NAME': AZURE_SQL_DATABASE,
                    'USER': user,
                    'PASSWORD': AZURE_SQL_PASSWORD,
                    'HOST': AZURE_SQL_HOST,
                    'PORT': os.environ.get('AZURE_SQL_PORT', ''),
                    'OPTIONS': {
                        'driver': os.environ.get('AZURE_ODBC_DRIVER', 'ODBC Driver 18 for SQL Server'),
                    },
                }

            # Postgres fallback (optional)
            if os.environ.get('POSTGRES_HOST'):
                return {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': os.environ.get('POSTGRES_DB'),
                    'USER': os.environ.get('POSTGRES_USER'),
                    'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
                    'HOST': os.environ.get('POSTGRES_HOST'),
                    'PORT': os.environ.get('POSTGRES_PORT', ''),
                }

            # Default: sqlite for local development
            return {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': str(BASE_DIR / 'db.sqlite3'),
            }


        DATABASES = {'default': get_database_config()}

        # Password validation
        AUTH_PASSWORD_VALIDATORS = [
            {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
            {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
            {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
            {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
        ]

        # Internationalization
        LANGUAGE_CODE = 'en-us'
        TIME_ZONE = 'UTC'
        USE_I18N = True
        USE_TZ = True

        # Static files
        STATIC_URL = 'static/'
        STATICFILES_DIRS = [BASE_DIR / 'static']

        DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
WSGI_APPLICATION = 'patientmanager.wsgi.application'



# Azure SQL env vars (set these to use Azure SQL)

AZURE_SQL_HOST = os.environ.get('AZURE_SQL_HOST')

