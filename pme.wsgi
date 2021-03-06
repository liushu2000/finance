import os
import sys
import site
import urllib

sys.stdout = sys.stderr

# Project root
root = '/var/www/ui_datatable_form'
sys.path.insert(0, root)

# Packages from virtualenv
activate_this = '/var/www/ui_datatable_form/pme_env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# Set environmental variable for Django and fire WSGI handler
os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings'
import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    environ['PATH_INFO'] = urllib.unquote(environ['REQUEST_URI'].split('?')[0])
    return _application(environ, start_response)
