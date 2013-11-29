from django.conf.urls import patterns, url


urlpatterns = patterns('fwadmin.views',

    # user stuff
    url(r'^$', 'index', name='index'),

    # hosts
    url(r'^host/new/$', 'new_host', name='new_host'),
    url(r'^host/(?P<pk>\d+)/edit/$', 'edit_host', name='edit_host'),
    url(r'^host/(?P<pk>\d+)/delete/$', 'delete_host', name='delete_host'),
    url(r'^host/(?P<pk>\d+)/renew/$', 'renew_host', name='renew_host'),
    # rules for the hosts
    url(r'^rule/new/(?P<hostid>\d+)/', 'new_rule_for_host',
        name="new_rule_for_host"),
    url(r'^rule/(?P<pk>\d+)/delete/', 'delete_rule', name="delete_rule"),

    # moderator views
    url(r'^host/(?P<pk>\d+)/approve/$', 'moderator_approve_host',
        name='moderator_approve_host'),
    url(r'^host/list/unapproved/$',
        'moderator_list_unapproved', name='moderator_list_unapproved'),
    url(r'^host/list/all/$',
        'moderator_list_all', name='moderator_list_all'),

)
