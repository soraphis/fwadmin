import datetime

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
    HostForm,
)


@login_required
def new_or_edit(request, ip=None):
    host = []
    if ip is not None:
        host = Host.objects.filter(ip=ip)
    if request.method == 'POST':
        form = HostForm(request.POST)
        if form.is_valid():
            # do not commit just yet, its not yet done
            host = form.save(commit=False)
            # add the auto calculated stuff
            host.owner = request.user
            host.active_until = datetime.datetime.now() + datetime.timedelta(
                days=365)
            host.save()
            # see https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
            form.save_m2m()
            return HttpResponseRedirect('/fwadmin/list/')
    else:
        if host:
            form = HostForm(instance=host[0])
        else:
            form = HostForm()
    return render_to_response('fwadmin/new.html', {'form': form },
                              context_instance=RequestContext(request))

@login_required
def list(request):
    queryset=Host.objects.filter(owner=request.user)
    return render_to_response('fwadmin/list.html', 
                              { 'all_hosts': queryset },
                              context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def list_unapproved(request):
    queryset=Host.objects.filter(approved=False)
    # XXX: add a template for list
    return render_to_response('fwadmin/list.html', 
                              { 'all_hosts': queryset },
                              context_instance=RequestContext(request))

