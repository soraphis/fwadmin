from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView

from fwadmin.models import Host

urlpatterns = patterns('fwadmin.views',
    # user stuff
    url(r'^new/$', 'new', name="new"),
    url(r'^list/$', 'list', name='list'),
    url(r'^edit/(?P<pk>\d+)/$', 'edit', name='edit'),
    url(r'^renew/(?P<pk>\d+)/$', 'renew', name='renew'),
    # admin stuff
    url(r'^admin-approve/(?P<pk>\d+)/$', 'approve', name='approve'),
    url(r'^admin-list-unapproved/$', 'list_unapproved', name='list_unapproved'),
    #url(r'^(?P<detail_id>\d+)/$', 'detail'),
    #url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    #url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)
