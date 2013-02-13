from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView

from fwadmin.models import Host

urlpatterns = patterns('fwadmin.views',
    url(r'^new/$', 'new', name="new"),
    url(r'^list/$', ListView.as_view(
            queryset=Host.objects.all(),
            context_object_name='all_hosts',
            template_name='fwadmin/list.html'),
        name="list",
        ),
    #url(r'^(?P<detail_id>\d+)/$', 'detail'),
    #url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    #url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)
