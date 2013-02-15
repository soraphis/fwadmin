from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView

from fwadmin.models import Host

urlpatterns = patterns('fwadmin.views',
    url(r'^new/$', 'new_or_edit', name="new"),
    url(r'^list/$', 'list', name='list'),
    url(r'^edit/(?P<ip>\d+\.\d+\.\d+\.\d+)/$', 'new_or_edit', name='edit'),
    #url(r'^(?P<detail_id>\d+)/$', 'detail'),
    #url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    #url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)
