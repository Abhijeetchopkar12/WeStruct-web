import os

from django.core.wsgi import get_wsgi_application

from django.utils.translation import _trans
_trans.get_language = lambda: 'en'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

application = get_wsgi_application()