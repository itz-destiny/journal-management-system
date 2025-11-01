# Add to your jms/settings.py

ALLOWED_HOSTS = ['acehq.pythonanywhere.com']

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = '/home/acehq/uniquejms/static'

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/acehq/uniquejms/media'

# Security settings
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True



