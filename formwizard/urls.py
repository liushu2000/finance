from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin
from django.contrib import admin
admin.autodiscover()

# js_info_dict = {
#     'packages': ('transjs.jsi18n',),
# }



urlpatterns = patterns('',
    # Examples:

    #url(r'^customers/', users_jqueryui, name='Customers'),
    #url(r'^login/$', 'django.contrib.auth.views.login', name="my_login"),


    url(r'^finance/', include('finance.urls')),
    # url(r'^formwizard/', include('formwizard.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # (r'^contact/$', 'contact.views.contact'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    # Django smart selects
    url(r'^chaining/', include('smart_selects.urls')),

    # (r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
    # Translation for outer js files
    # url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    # django-selectable
    (r'^selectable/', include('selectable.urls')),
)
