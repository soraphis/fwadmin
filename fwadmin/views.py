from django.http import (
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
    HostForm,
)


@login_required
def new(request):
    if request.method == 'POST':
        form = HostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('fwadmin/list/')
    else:
        form = HostForm()
    return render_to_response('fwadmin/new.html', {'form': form },
                              context_instance=RequestContext(request))

