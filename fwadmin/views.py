import datetime
from django.utils.translation import ugettext as _

from django.http import (
    HttpResponse,
    HttpResponseRedirect, 
    HttpResponseForbidden,
)
from django.shortcuts import (
    render_to_response, 
    redirect,
)
from django.template import RequestContext
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)

from fwadmin.forms import (
    Host,
    NewHostForm,
    EditHostForm,
)

def is_in_ldap_group(user, group_name):
    if user:
        return user.groups.filter(name=group_name).count() == 1
    return False


@login_required
@user_passes_test(lambda u: is_in_ldap_group(u, "Mitarb"))
def index(request):
    return render_to_response('fwadmin/index.html', 
                              context_instance=RequestContext(request))


@login_required
def list(request):
    queryset=Host.objects.filter(owner=request.user)
    return render_to_response('fwadmin/list.html', 
                              { 'all_hosts': queryset },
                              context_instance=RequestContext(request))


@login_required
def new(request, pk=None):
    if request.method == 'POST':
        form = NewHostForm(request.POST)
        if form.is_valid():
            # do not commit just yet, its not yet done
            host = form.save(commit=False)
            # add the stuff here that the user can't edit
            host.owner = request.user
            active_until = datetime.date.today() + datetime.timedelta(365)
            host.active_until = active_until
            # and really save
            host.save()
            # see https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
            form.save_m2m()
            return HttpResponseRedirect('/fwadmin/list/')
    form = NewHostForm()
    return render_to_response('fwadmin/new.html',
                              {'form': form,
                               'action': _("New Host"),
                              },
                              context_instance=RequestContext(request))


@login_required
def edit(request, pk):
    host = Host.objects.filter(pk=pk)[0]
    if host.owner != request.user:
        return HttpResponseForbidden("you are not owner")
    if request.method == 'POST':
        form = EditHostForm(request.POST, instance=host)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/fwadmin/list/')
        return  HttpResponseRedirect('/fwadmin/list/')
    form = EditHostForm(instance=host)
    return render_to_response('fwadmin/new.html',
                              {'form': form,
                               'action': _("Edit Host"),
                              },
                              context_instance=RequestContext(request))


@login_required
def renew(request, pk):
    host = Host.objects.filter(pk=pk)[0]
    if host.owner != request.user:
        return HttpResponseForbidden("you are not owner")
    active_until = datetime.date.today() + datetime.timedelta(365)
    host.active_until = active_until
    host.save()
    return render_to_response('fwadmin/renewed.html',
                              { 'active_until': active_until},
                              context_instance=RequestContext(request))
    

@user_passes_test(lambda u: u.is_superuser)
def list_unapproved(request):
    queryset=Host.objects.filter(approved=False)
    # XXX: add a template for list
    return render_to_response('fwadmin/list-unapproved.html', 
                              { 'all_hosts': queryset },
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def approve(request, pk):
    host = Host.objects.filter(pk=pk)[0]
    host.approved = True
    host.save()
    return redirect('/fwadmin/admin-list-unapproved/',
                    context_instance=RequestContext(request))
