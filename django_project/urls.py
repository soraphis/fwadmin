from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns

# enable admin interface
from django.contrib import admin
admin.autodiscover()

urlpatterns = i18n_patterns('',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^django_project/', include('django_project.foo.urls')),

    url(r'^$', RedirectView.as_view(url='/fwadmin/')),
    url(r'^fwadmin/',
        include('fwadmin.urls', namespace="fwadmin")),

    # login handling
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'fwadmin/login.html'},
        name='login'),

    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
