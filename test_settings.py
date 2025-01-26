"""
These settings are here to use during tests, because django requires them.

In a real-world use case, apps in this project are installed into other
Django applications, so these settings will not be used.
"""

from os.path import abspath, dirname, join


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'default.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}



INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'message_q_app',
)

LOCALE_PATHS = [
    root('message_q_app', 'conf', 'locale'),
]



ROOT_URLCONF = 'message_q_app.urls'

SECRET_KEY = 'insecure-secret-key'

DEBUG = True
ALLOWED_HOSTS = ['*']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Add the templates directory relative to the base directory
            root('message_q_app', 'templates'),
        ],
        'APP_DIRS': True,  # This allows Django to look for templates inside each app's templates folder
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