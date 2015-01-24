#!/usr/bin/python
import warnings
import os
import sys
warnings.simplefilter("ignore", DeprecationWarning)
warnings.filterwarnings("ignore", ".*Module _mysql was already imported.*")
warnings.filterwarnings("ignore", ".*Module timezones was already imported.*")

project = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(project, 'droptour'))
#sys.path.append(os.path.join(project, ''))

os.environ['DJANGO_SETTINGS_MODULE'] = 'droptour.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
