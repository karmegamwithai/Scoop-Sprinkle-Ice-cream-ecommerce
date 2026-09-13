import os
import sys

# Project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project root to Python path
sys.path.insert(0, PROJECT_ROOT)

# Tell Django which settings to use
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "icecream_shop.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()