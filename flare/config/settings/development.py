from .base import *  # noqa

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'app']  # ["*"]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
