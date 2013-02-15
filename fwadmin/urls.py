from django.conf.urls import patterns, url


urlpatterns = patterns('fwadmin.views',
    # user stuff
    url(r'^$', 'list', name='list'),
    url(r'^list/$', 'list', name='list'),

    url(r'^new/$', 'new', name="new"),
    url(r'^edit/(?P<pk>\d+)/$', 'edit', name='edit'),
    url(r'^renew/(?P<pk>\d+)/$', 'renew', name='renew'),
    # admin stuff
    url(r'^admin-approve/(?P<pk>\d+)/$', 'approve', name='approve'),
    url(r'^admin-list-unapproved/$', 'list_unapproved', name='list_unapproved'),
)
