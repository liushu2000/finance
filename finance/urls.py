from django.conf.urls import patterns, include, url
from regression2 import company_monthly



urlpatterns = patterns('',

    # url(r'^$', 'auth.views.user', name='user'),

    url(r'^monthly/$', company_monthly, name='company_monthly'),

    )
