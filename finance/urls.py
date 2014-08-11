from django.conf.urls import patterns, include, url
from regression2 import company_monthly
from views import *



urlpatterns = patterns('',


    url(r'^monthly/$', company_monthly, name='company_monthly'),
    url(r'^group/$', make_groups, name='make_groups'),

    )
