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
from django.contrib.auth.decorators import login_required

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
            host = form.save(commit=False)
            # add owner as its not part of the form itself
            host.owner = request.user
            host.save()
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
    # XXX: query only hosts for the given user
    queryset=Host.objects.filter(owner=request.user)
    return render_to_response('fwadmin/list.html', 
                              { 'all_hosts': queryset },
                              context_instance=RequestContext(request))

