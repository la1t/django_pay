import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True
SECRET_KEY = "DEBUG SECRET KEY"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_pay2",
    "orders",
]

ROOT_URLCONF = "urls"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# DATABASES
# ------------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_URL = "/static/"

# DJANGO_PAY2
# ------------------------------------------------------------------------------
PAYMENTS = {
    "DEBUG_MODE": bool(os.environ.get("DJANGO_PAY_DEBUG")),
    "TINKOFF": {
        "terminal_key": os.environ.get("TINKOFF_TERMINAL_KEY"),
        "password": os.environ.get("TINKOFF_PASSWORD"),
        "email_company": os.environ.get("TINKOFF_EMAIL_COMPANY"),
        "taxation": os.environ.get("TINKOFF_TAXATION"),
    },
}
