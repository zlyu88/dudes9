import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'your_host',
        'USER': 'your_user',
        'PASSWORD': 'your_user_password',
        'NAME': 'your_database_name',
    }
}

DEBUG = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mail.com'
EMAIL_HOST_USER = 'your@mail.com'
EMAIL_HOST_PASSWORD = 'your_mail_password'
EMAIL_PORT = 'your_port'
