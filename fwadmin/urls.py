from django.conf.urls import patterns, url


urlpatterns = patterns('fwadmin.views',

    # user stuff
    url(r'^$', 'index', name='index'),

    # special
    url(r'^export/(?P<fwtype>\w+)/$', 'export', name='export'),
    url(r'^export_via_token/(?P<fwtype>\w+)/(?P<export_token>[-\w]+)/$',
        'export_via_token', name='export_via_token'),

    # hosts
    url(r'^host/new/$', 'new_host', name='new_host'),
    url(r'^host/(?P<pk>\d+)/edit/$', 'edit_host', name='edit_host'),
    url(r'^host/(?P<pk>\d+)/delete/$', 'delete_host', name='delete_host'),
    url(r'^host/(?P<pk>\d+)/renew/$', 'renew_host', name='renew_host'),
    # rules for the hosts
    url(r'^host/(?P<hostid>\d+)/rule/new/', 'new_rule_for_host',
        name="new_rule_for_host"),
    url(r'^rule/(?P<pk>\d+)/delete/', 'delete_rule', name="delete_rule"),

    # lookup
    url(r'^gethostbyname/(?P<hostname>[\w_.-]+)/$',
        'gethostbyname', name="gethostbyname"),

    # moderator views
    url(r'^admin/host/(?P<pk>\d+)/approve/$', 'moderator_approve_host',
        name='moderator_approve_host'),
    url(r'^admin/host/$',
        'moderator_list_all', name='moderator_list_all'),
    url(r'^admin/host/unapproved/$',
        'moderator_list_unapproved', name='moderator_list_unapproved'),

)
