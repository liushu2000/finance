from django.conf.urls import patterns, include, url
from forms import *
from views import *
from django.contrib.auth.models import User

urlpatterns = patterns('',
    
    url(r'^$', 'group.views.group', name='group'),


    # url(r'^register/$', 'auth.views.user_register'),
    # url(r'^create/$', 'auth.views.create_user'),
    url(r'^create/$',  (login_required(CreateGroupWizard.as_view([GroupCreationForm, ])))),
    url(r'^(?P<group_id_branch>\d+)/branch/create/$',  (login_required(CreateGroupWizard.as_view([GroupCreationForm, ])))),
    url(r'^edit/(?P<group_id>\d+)/$',  (login_required(CreateGroupWizard.as_view([GroupCreationForm, ])))),
    # (r'^edit/(?P<user_id>\d+)/$', edit_user, {}, 'edit_user'),
    url(r'^group_list_json/', GroupListJson.as_view(), name="group_list_json"),
    )