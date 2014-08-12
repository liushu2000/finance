from django.conf.urls import patterns, include, url
from regression2 import company_monthly
from views import *
from import_data import *
from regression import *

urlpatterns = patterns('',

    url(r'^$', home, name='home'),
    url(r'^monthly/$', company_monthly, name='company_monthly'),
    url(r'^monthly_vp/$', monthly_vp, name='monthly_vp'),
    url(r'^import/$', import_data, name='import_data'),
    url(r'^regression/$', regression, name='regression'),
    )
