from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext

from fwadmin.models import (
    Host,
    Port,
)
from fwadmin.forms import (
    HostForm,
)

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
